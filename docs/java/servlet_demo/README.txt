# what is servlet? The following is the code of Servlet:
#############################################################
public interface Servlet {
    void init(ServletConfig var1) throws ServletException;

    ServletConfig getServletConfig();

    void service(ServletRequest var1, ServletResponse var2) throws ServletException, IOException;

    String getServletInfo();

    void destroy();
}
#############################################################

# so it just a interface in java with 5 methods
# but there are many classes have implemented this interface
# so what we need to do is just extend from them