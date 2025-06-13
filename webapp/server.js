const { createServer } = require('http')
const { parse } = require('url')
const next = require('next')
const WebSocket = require('ws')

const dev = process.env.NODE_ENV !== 'production'
const hostname = 'localhost'
const port = 3000

const app = next({ dev, hostname, port })
const handle = app.getRequestHandler()

app.prepare().then(() => {
  const server = createServer(async (req, res) => {
    try {
      const parsedUrl = parse(req.url, true)
      await handle(req, res, parsedUrl)
    } catch (err) {
      console.error('Error occurred handling', req.url, err)
      res.statusCode = 500
      res.end('internal server error')
    }
  })

  // Create WebSocket server
  const wss = new WebSocket.Server({ noServer: true })

  wss.on('connection', (ws) => {
    console.log('Client connected to WebSocket proxy')
    
    // Create connection to backend WebSocket
    const backendWs = new WebSocket('ws://localhost:8080/api/v1/ws')
    
    backendWs.on('open', () => {
      console.log('Connected to backend WebSocket')
    })
    
    // Relay messages from client to backend
    ws.on('message', (message) => {
      if (backendWs.readyState === WebSocket.OPEN) {
        backendWs.send(message)
      }
    })
    
    // Relay messages from backend to client
    backendWs.on('message', (message) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(message)
      }
    })
    
    // Handle errors
    backendWs.on('error', (error) => {
      console.error('Backend WebSocket error:', error)
      ws.close()
    })
    
    ws.on('error', (error) => {
      console.error('Client WebSocket error:', error)
      backendWs.close()
    })
    
    // Handle disconnections
    backendWs.on('close', () => {
      ws.close()
    })
    
    ws.on('close', () => {
      backendWs.close()
    })
  })

  // Handle WebSocket upgrade
  server.on('upgrade', (request, socket, head) => {
    const { pathname } = parse(request.url)
    console.log('WebSocket upgrade request for:', pathname)
    
    if (pathname === '/ws') {
      wss.handleUpgrade(request, socket, head, (ws) => {
        wss.emit('connection', ws)
      })
    } else {
      socket.destroy()
    }
  })

  server.listen(port, (err) => {
    if (err) throw err
    console.log(`> Ready on http://${hostname}:${port}`)
    console.log('> WebSocket proxy ready on /ws')
  })
})