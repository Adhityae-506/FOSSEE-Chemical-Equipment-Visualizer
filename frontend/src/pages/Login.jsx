// import React, { useState, useContext } from "react";
// import { AuthContext } from "../contexts/AuthContext";
// import { useNavigate } from "react-router-dom";

// export default function Login(){
//   const { login } = useContext(AuthContext);
//   const [username, setU] = useState("");
//   const [password, setP] = useState("");
//   const [error, setError] = useState(null);
//   const nav = useNavigate();

//   const submit = async (e) => {
//     e.preventDefault();
//     try {
//       await login(username, password);
//       nav("/");
//     } catch (err) {
//       setError(err.payload || err.message);
//     }
//   };

//   return (
//     <div className="login">
//       <h2>Sign in</h2>
//       <form onSubmit={submit}>
//         <input value={username} onChange={e=>setU(e.target.value)} placeholder="username" />
//         <input value={password} onChange={e=>setP(e.target.value)} type="password" placeholder="password" />
//         <button type="submit">Login</button>
//         {error && <div className="error">{JSON.stringify(error)}</div>}
//       </form>
//     </div>
//   );
// }

// import React, { useState, useContext } from "react";
// import { AuthContext } from "../contexts/AuthContext";
// import Button from "../ui/Button";
// import Input from "../ui/Input";
// import Card from "../ui/Card";
// import "./Login.css";

// export default function Login() {
//   const { login, loading } = useContext(AuthContext);
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");

//   const handleLogin = async () => {
//     await login(username, password);
//   };

//   return (
//     <div className="login-wrapper">
//       <Card style={{ width: "380px", textAlign: "center" }}>
//         <h2 style={{ color: "var(--primary)" }}>Sign in</h2>

//         <Input
//           placeholder="Username"
//           value={username}
//           onChange={(e) => setUsername(e.target.value)}
//         />

//         <Input
//           type="password"
//           placeholder="Password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//         />

//         <Button onClick={handleLogin}>
//           {loading ? "Logging in..." : "Login"}
//         </Button>
//       </Card>
//     </div>
//   );
// }


// import React, { useState, useContext } from "react";
// import { AuthContext } from "../contexts/AuthContext";
// import Button from "../ui/Button";
// import Input from "../ui/Input";
// import Card from "../ui/Card";
// import "./Login.css";

// export default function Login() {
//   const { login, loading } = useContext(AuthContext);

//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState(null);

//   const handleLogin = async () => {
//     try {
//       await login(username, password);
//     } catch (err) {
//       setError("Invalid username or password");
//     }
//   };

//   return (
//     <div className="login-wrapper">
//       <Card className="login-card">
//         <h2 className="login-title">Welcome Back</h2>

//         <Input
//           placeholder="Username"
//           value={username}
//           onChange={(e) => setUsername(e.target.value)}
//         />

//         <Input
//           type="password"
//           placeholder="Password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//         />

//         <Button onClick={handleLogin}>
//           {loading ? "Logging in..." : "Login"}
//         </Button>

//         {error && <p className="login-error">{error}</p>}
//       </Card>
//     </div>
//   );
// }


import React, { useState, useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";
import Button from "../ui/Button";
import Input from "../ui/Input";
import Card from "../ui/Card";
import "./Login.css";

export default function Login() {
  const { login, loading } = useContext(AuthContext);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    try {
      await login(username, password);
      setError(null);
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="login-wrapper">
      {/* Top greeting section */}
      <div className="login-text">
        <h1 className="login-heading">Welcome to Chemical Equipment Visualizer</h1>
        <p className="login-subtitle">
          Sign in using the credentials provided by your instructor or system
          administrator to upload datasets and view interactive reports.
        </p>
      </div>

      {/* Login card */}
      <Card className="login-card">
        <h2 className="login-title">Sign in</h2>

        <Input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <Button onClick={handleLogin} style={{ width: "100%", marginTop: "8px" }}>
          {loading ? "Logging in..." : "Login"}
        </Button>

        {error && <p className="login-error">{error}</p>}
      </Card>
    </div>
  );
}
