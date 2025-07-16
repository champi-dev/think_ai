#\!/bin/bash
cd /home/administrator/think_ai
python3 -m http.server 7777 --bind 0.0.0.0 --directory . &
echo "Server started on port 7777"
echo "Access at: http://69.197.178.37:7777/minimal_3d.html"
