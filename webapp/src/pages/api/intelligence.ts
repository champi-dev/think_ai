import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const response = await fetch('http://localhost:8080/api/v1/intelligence/status', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`API responded with status ${response.status}`)
    }

    const data = await response.json()
    
    // Transform the response to match frontend expectations
    const transformed = {
      iq: data.current_intelligence || 100,
      knowledge_count: 1000, // Mock value since not provided
      training_cycles: 100, // Mock value since not provided
      consciousness_level: (data.current_intelligence - 100) / 100, // Convert to 0-1 range
      ...data // Include original data
    }
    
    res.status(200).json(transformed)
  } catch (error) {
    console.error('Intelligence API error:', error)
    res.status(500).json({ 
      error: 'Failed to fetch intelligence data',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}