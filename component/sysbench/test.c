
/***********************************************************************
  module:       test.c
  description:  test UNIX sockets.
  time:         2023-01-16
  build:        gcc -o test test.c
  trace:        strace -e all -o strace.log ./test 127.0.0.1
 ***********************************************************************/
 
#include "socket.c"

int main(int argc, char *argv[])
{
    printf("argc count: %d\r\n", argc);
    if (argc > 1)
    {
         printf("argv[1]: %s\r\n", argv[1]);
    }
    char host[1024] = "127.0.0.1";
    int port=8085;
    int s = Socket(host, port);
    printf("socket: %d\n", s);
    if(s<0){printf("connect error: %d", s);return -1;}
    char buf[1500];
    memset(buf,0,1500);
    int i;
    char request[2048];
    memset(request,0,2048);
    char url[100] = "http://127.0.0.1:8019/gofs/check";
    i = strstr(url, "://") -url + 3;
    printf("-- %d\n", strstr(url, "://") - url);
    printf("i: %d\n", i);  
    strcpy(request, "GET");
    strcat(request, " ");  
    strcat(request, "/go/check HTTP/1.0\r\n");
    strcat(request, "Host: 127.0.0.1\r\n");
    strcat(request, "\r\n");
    // strcat(request, "Connection: close\r\n");
    printf("request: \n%s\n", request);
    printf("rlen: %d", strlen(request));
    //return 0;
    int r_len = write(s, request, strlen(request));
    printf("rlen: %d %d", r_len, strlen(request)); 
    if (r_len != strlen(request))
    {
        printf("request error\n");
        close(s);
    }
    // i = read(s, buf, 1500);
    char ch;
    while(1)
    {
        i = read(s, &ch, 1);
        if(i<=0){break;}
        printf("%c", ch);
    }
    close(s);
    printf("\n");
    return 0;
}

