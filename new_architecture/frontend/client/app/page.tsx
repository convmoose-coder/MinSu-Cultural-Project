'use client'

import { useState, useEffect } from 'react'
import Head from 'next/head'

export default function Home() {
  const [cultures, setCultures] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 这里应该从API获取数据
    // 暂时使用模拟数据
    const mockData = [
      { id: 1, name: '北京四合院文化', description: '体验老北京的传统居住文化' },
      { id: 2, name: '云南古城民宿', description: '感受彩云之南的独特魅力' },
      { id: 3, name: '江南水乡风情', description: '领略小桥流水人家的诗意' },
    ]
    setCultures(mockData)
    setLoading(false)
  }, [])

  return (
    <>
      <Head>
        <title>民宿文化平台</title>
        <meta name="description" content="探索中国各地的民宿文化和传统" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">欢迎来到民宿文化平台</h1>
        
        {loading ? (
          <p className="text-center">加载中...</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cultures.map((culture) => (
              <div key={culture.id} className="border rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
                <h2 className="text-2xl font-semibold mb-2">{culture.name}</h2>
                <p className="text-gray-600 mb-4">{culture.description}</p>
                <button className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
                  了解更多
                </button>
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  )
}