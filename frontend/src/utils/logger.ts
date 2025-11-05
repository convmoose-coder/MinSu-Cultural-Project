/**
 * 前端日志工具类
 * 提供不同级别的日志记录功能，便于调试和问题排查
 */

// 日志级别枚举
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error',
  FATAL = 'fatal'
}

// 默认日志级别
let currentLevel = LogLevel.DEBUG;

// 格式化时间戳
function formatTimestamp(): string {
  const now = new Date();
  return now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
}

// 格式化日志消息
function formatMessage(level: LogLevel, module: string, message: string, data?: any): string {
  const timestamp = formatTimestamp();
  let logMessage = `[${timestamp}] [${level.toUpperCase()}] [${module}] ${message}`;
  
  if (data !== undefined) {
    logMessage += `\nData: ${typeof data === 'string' ? data : JSON.stringify(data, null, 2)}`;
  }
  
  return logMessage;
}

// 检查日志级别是否应该输出
function shouldLog(level: LogLevel): boolean {
  const levels = Object.values(LogLevel);
  return levels.indexOf(level) >= levels.indexOf(currentLevel);
}

/**
 * 日志工具类
 */
export class Logger {
  private module: string;
  
  constructor(module: string) {
    this.module = module;
  }
  
  /**
   * 调试级别日志
   * @param message 日志消息
   * @param data 附加数据
   */
  debug(message: string, data?: any): void {
    if (shouldLog(LogLevel.DEBUG)) {
      console.debug(formatMessage(LogLevel.DEBUG, this.module, message, data));
    }
  }
  
  /**
   * 信息级别日志
   * @param message 日志消息
   * @param data 附加数据
   */
  info(message: string, data?: any): void {
    if (shouldLog(LogLevel.INFO)) {
      console.info(formatMessage(LogLevel.INFO, this.module, message, data));
    }
  }
  
  /**
   * 警告级别日志
   * @param message 日志消息
   * @param data 附加数据
   */
  warn(message: string, data?: any): void {
    if (shouldLog(LogLevel.WARN)) {
      console.warn(formatMessage(LogLevel.WARN, this.module, message, data));
    }
  }
  
  /**
   * 错误级别日志
   * @param message 日志消息
   * @param error 错误对象或附加数据
   */
  error(message: string, error?: any): void {
    if (shouldLog(LogLevel.ERROR)) {
      console.error(formatMessage(LogLevel.ERROR, this.module, message, error));
    }
  }
  
  /**
   * 致命错误级别日志
   * @param message 日志消息
   * @param error 错误对象或附加数据
   */
  fatal(message: string, error?: any): void {
    if (shouldLog(LogLevel.FATAL)) {
      console.error(formatMessage(LogLevel.FATAL, this.module, message, error));
    }
  }
  
  /**
   * 记录API调用
   * @param endpoint API端点
   * @param method HTTP方法
   * @param request 请求数据
   * @param response 响应数据
   * @param duration 响应时间(毫秒)
   */
  apiCall(
    endpoint: string, 
    method: string, 
    request?: any, 
    response?: any, 
    duration?: number
  ): void {
    if (shouldLog(LogLevel.INFO)) {
      const message = `API ${method.toUpperCase()} ${endpoint}`;
      const data = {
        method,
        endpoint,
        request,
        response: response ? { status: response.status, data: response.data } : undefined,
        duration: `${duration}ms`
      };
      console.info(formatMessage(LogLevel.INFO, this.module, message, data));
    }
  }
  
  /**
   * 记录API错误
   * @param endpoint API端点
   * @param method HTTP方法
   * @param error 错误信息
   * @param request 请求数据
   */
  apiError(endpoint: string, method: string, error: any, request?: any): void {
    if (shouldLog(LogLevel.ERROR)) {
      const message = `API Error ${method.toUpperCase()} ${endpoint}`;
      const data = {
        method,
        endpoint,
        request,
        error: error instanceof Error ? {
          message: error.message,
          stack: error.stack
        } : error
      };
      console.error(formatMessage(LogLevel.ERROR, this.module, message, data));
    }
  }
}

/**
 * 设置全局日志级别
 * @param level 日志级别
 */
export function setLogLevel(level: LogLevel): void {
  currentLevel = level;
  console.log(`日志级别已设置为: ${level}`);
}

/**
 * 创建日志实例
 * @param module 模块名称
 * @returns Logger实例
 */
export function createLogger(module: string): Logger {
  return new Logger(module);
}

export default createLogger;
