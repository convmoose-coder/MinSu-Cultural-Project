// 民俗文化类型定义
export type FolkCulture = {
  id: number;
  title: string;
  description: string;
  category: string;
  region: string;
  created_at?: string;
};

export type FolkCultureCreate = {
  title: string;
  description: string;
  category: string;
  region: string;
};

export type FolkCultureResponse = {
  id: number;
  title: string;
  message: string;
};