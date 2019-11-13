1. 以管理员身份运行
2. docker等依赖hyperV的程序会无法运行，请注意。
3. 如果想重启hyperV，可以用管理员身份运行Powershell，然后输入
	Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All 
	重启即可。