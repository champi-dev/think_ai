export default function Test() {
  return (
    <div style={{ padding: "20px", color: "white", backgroundColor: "black" }}>
      <h1>Think AI v3.1.0 Test Page</h1>
      <p>If you can see this, the webapp is running!</p>
      <p>
        API URL: {process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080"}
      </p>
    </div>
  );
}
