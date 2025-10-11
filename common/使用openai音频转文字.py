from openai import OpenAI
from pydub import AudioSegment
import math
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading
import time

# 繁体转简体映射（常用字）
def traditional_to_simplified(text):
    """
    将繁体中文转换为简体中文
    使用 opencc-python-reimplemented 库（需要安装: pip install opencc-python-reimplemented）
    如果没有安装该库，会使用内置的基础转换
    """
    try:
        from opencc import OpenCC
        cc = OpenCC('t2s')  # t2s = Traditional to Simplified
        return cc.convert(text)
    except ImportError:
        # 如果没有安装 opencc，提示用户安装
        print("⚠️  建议安装 opencc-python-reimplemented 以获得更好的繁简转换效果")
        print("   安装命令: pip install opencc-python-reimplemented")
        # 返回原文本
        return text

# 初始化 OpenAI 客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 线程锁，用于保护共享资源
lock = threading.Lock()

def split_audio(file_path, chunk_length_ms=60000):
    """
    把音频切分成小段，默认每段 60 秒
    """
    print("🎵 正在加载音频文件...")
    audio = AudioSegment.from_file(file_path)
    total_chunks = math.ceil(len(audio) / chunk_length_ms)
    chunks = []

    print(f"📊 音频总时长: {len(audio) / 1000:.1f} 秒")
    print(f"✂️  将切分为 {total_chunks} 段 (每段 {chunk_length_ms/1000:.0f} 秒)")

    # 使用进度条显示切分进度
    with tqdm(total=total_chunks, desc="切分音频", unit="段", ncols=80) as pbar:
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i+chunk_length_ms]
            chunk_name = f"chunk_{i//chunk_length_ms:03d}.mp3"
            chunk.export(chunk_name, format="mp3")
            chunks.append(chunk_name)
            pbar.update(1)

    print(f"✅ 音频切分完成，生成 {len(chunks)} 个片段文件")
    return chunks

def transcribe_single_chunk(chunk_info):
    """
    转写单个音频片段
    chunk_info: (index, filename, start_time_seconds) 元组
    """
    idx, chunk_file, start_time = chunk_info
    
    try:
        with open(chunk_file, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="zh",  # 指定中文
                response_format="text"  # 直接获取文本
            )
        
        # 转换为简体中文
        simplified_text = traditional_to_simplified(transcript)
        
        return idx, simplified_text, start_time, None
    except Exception as e:
        return idx, None, start_time, str(e)

def transcribe_audio_threaded(chunks, max_workers=4, chunk_length_seconds=60):
    """
    使用多线程转写音频片段
    """
    total_chunks = len(chunks)
    results = {}  # 改为字典，用索引作为键
    errors = []
    
    print(f"🚀 开始多线程转写，使用 {max_workers} 个线程")
    print(f"📝 共需处理 {total_chunks} 个音频片段")
    
    # 准备任务数据：(索引, 文件名, 开始时间)
    chunk_tasks = [
        (i, chunk, i * chunk_length_seconds) 
        for i, chunk in enumerate(chunks)
    ]
    
    # 使用线程池和进度条
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_chunk = {
            executor.submit(transcribe_single_chunk, task): task 
            for task in chunk_tasks
        }
        
        # 使用进度条显示转写进度
        with tqdm(total=total_chunks, desc="转写进度", unit="段", ncols=80) as pbar:
            for future in as_completed(future_to_chunk):
                chunk_info = future_to_chunk[future]
                try:
                    idx, text, start_time, error = future.result()
                    if error:
                        errors.append(f"片段 {idx}: {error}")
                        pbar.write(f"❌ 片段 {idx} 转写失败: {error}")
                    else:
                        # 格式化时间戳
                        minutes, seconds = divmod(start_time, 60)
                        hours, minutes = divmod(minutes, 60)
                        timestamp = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
                        
                        # 存储为字典，确保按索引排序
                        results[idx] = (timestamp, text)
                        
                        # 显示部分转写结果预览（限制字符数避免输出过长）
                        preview = text[:40] + "..." if len(text) > 40 else text
                        pbar.write(f"✅ [{timestamp}] 片段 {idx:3d}: {preview}")
                    
                except Exception as e:
                    idx = chunk_info[0]
                    errors.append(f"片段 {idx}: {str(e)}")
                    pbar.write(f"💥 片段 {idx} 处理异常: {str(e)}")
                
                pbar.update(1)
    
    # 检查是否有失败的片段
    if errors:
        print(f"\n⚠️  有 {len(errors)} 个片段转写失败:")
        for error in errors:
            print(f"   {error}")
    
    # 按索引顺序排序并返回结果
    sorted_results = []
    for i in range(total_chunks):
        if i in results:
            sorted_results.append(results[i])
    
    print(f"\n📊 转写统计:")
    print(f"   成功: {len(sorted_results)}/{total_chunks} 个片段")
    print(f"   失败: {len(errors)} 个片段")
    
    return sorted_results

def merge_text(results, output_file="transcript.txt"):
    """
    合并所有片段文字并保存，包含时间戳
    results: 包含 (timestamp, text) 元组的列表
    """
    if not results:
        print("❌ 没有可用的转写结果")
        return None
        
    print(f"📝 正在合并 {len(results)} 段文字...")
    
    # 构建包含时间戳的完整文本
    formatted_segments = []
    for timestamp, text in results:
        formatted_segments.append(f"[{timestamp}] {text}")
    
    full_text = "\n\n".join(formatted_segments)
    
    # 同时创建一个不带时间戳的纯文本版本
    pure_text = "\n\n".join([text for _, text in results])
    
    # 保存带时间戳版本（使用 UTF-8 编码确保中文正确显示）
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    # 保存纯文本版本
    pure_text_file = output_file.replace('.txt', '_pure.txt')
    with open(pure_text_file, "w", encoding="utf-8") as f:
        f.write(pure_text)
    
    # 计算统计信息
    word_count = len(pure_text.split())
    char_count = len(pure_text)
    
    print(f"✅ 转写完成!")
    print(f"📄 文件保存:")
    print(f"   带时间戳: {output_file}")
    print(f"   纯文本版: {pure_text_file}")
    print(f"📊 统计信息:")
    print(f"   字符数: {char_count:,}")
    print(f"   词语数: {word_count:,}")
    
    return output_file

def cleanup_chunks(chunks):
    """
    清理临时音频片段文件
    """
    print("🧹 清理临时文件...")
    cleaned = 0
    for chunk in chunks:
        try:
            if os.path.exists(chunk):
                os.remove(chunk)
                cleaned += 1
        except Exception as e:
            print(f"⚠️  无法删除 {chunk}: {e}")
    
    print(f"✅ 已清理 {cleaned} 个临时文件")

def main():
    # 配置参数
    input_file = "/Users/SomeUser/Downloads/output-2.m4a"  # 修改为你的音频文件路径
    chunk_length_seconds = 60      # 每段音频长度（秒）
    max_workers = 16                # 最大线程数
    output_file = "transcript.txt" # 输出文件名
    cleanup_temp_files = True      # 是否清理临时文件
    
    print("🎙️  语音转文字工具 (多线程版 - 简体中文)")
    print("=" * 50)
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"❌ 错误: 找不到音频文件 '{input_file}'")
        print("请修改脚本中的 input_file 变量为正确的文件路径")
        return
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误: 未设置 OPENAI_API_KEY 环境变量")
        print("请设置环境变量: export OPENAI_API_KEY='your-api-key'")
        return
    
    try:
        start_time = time.time()
        
        # 步骤1: 切分音频
        chunks = split_audio(input_file, chunk_length_ms=chunk_length_seconds*1000)
        
        # 步骤2: 多线程转写
        results = transcribe_audio_threaded(chunks, max_workers=max_workers, 
                                          chunk_length_seconds=chunk_length_seconds)
        
        # 步骤3: 合并结果
        final_output = merge_text(results, output_file)
        
        # 步骤4: 清理临时文件
        if cleanup_temp_files:
            cleanup_chunks(chunks)
        
        # 显示总耗时
        total_time = time.time() - start_time
        print(f"\n⏱️  总耗时: {total_time:.1f} 秒")
        
        if final_output:
            print(f"🎉 全部完成! 结果保存在: {final_output}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断操作")
        if 'chunks' in locals():
            cleanup_chunks(chunks)
    except Exception as e:
        print(f"\n💥 发生错误: {str(e)}")
        if 'chunks' in locals():
            cleanup_chunks(chunks)

if __name__ == "__main__":
    main()