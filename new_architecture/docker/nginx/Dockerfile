# 使用官方Nginx镜像作为基础镜像
FROM nginx:alpine

# 删除默认的Nginx配置文件
RUN rm /etc/nginx/conf.d/default.conf

# 复制自定义Nginx配置文件
COPY nginx.conf /etc/nginx/conf.d/