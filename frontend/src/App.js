import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import * as THREE from "three";
import "./App.css";

const API = "https://hacer910-lupus-detector.hf.space";

function hashPw(pw) {
  let hash = 0;
  for (let i = 0; i < pw.length; i++) {
    hash = ((hash << 5) - hash) + pw.charCodeAt(i);
    hash |= 0;
  }
  return hash.toString();
}

// ── THREE.JS HERO ──────────────────────────────────────────
function ThreeHero() {
  const canvasRef = useRef(null);
  const tooltipRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const hero = canvas.parentElement;
    const W = hero.offsetWidth, H = hero.offsetHeight;
    canvas.width = W; canvas.height = H;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(W, H);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, W / H, 0.1, 100);
    camera.position.z = 5;

    const objects = [];
    const tips = [
      "YOLOv8 Neural Network\nReal-time classification",
      "Confidence Scoring\n96.8% accuracy rate",
      "Medical Imaging\nDermoscopic analysis"
    ];

    const ico = new THREE.Mesh(new THREE.IcosahedronGeometry(0.7, 0), new THREE.MeshBasicMaterial({ color: 0xef4444, wireframe: true, transparent: true, opacity: 0.6 }));
    ico.position.set(-2.8, 0.4, -1);
    scene.add(ico);
    const icoIn = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 0), new THREE.MeshBasicMaterial({ color: 0x1a0000, transparent: true, opacity: 0.8 }));
    icoIn.position.copy(ico.position);
    scene.add(icoIn);
    objects.push({ mesh: ico, inner: icoIn, tip: tips[0], speed: 0.008, axis: new THREE.Vector3(1, 1, 0).normalize(), base: ico.position.clone() });

    const tor = new THREE.Mesh(new THREE.TorusKnotGeometry(0.5, 0.12, 80, 12), new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.15 }));
    tor.position.set(2.8, -0.2, -1);
    scene.add(tor);
    objects.push({ mesh: tor, inner: null, tip: tips[1], speed: 0.006, axis: new THREE.Vector3(0.5, 1, 0.3).normalize(), base: tor.position.clone() });

    const oct = new THREE.Mesh(new THREE.OctahedronGeometry(0.45, 0), new THREE.MeshBasicMaterial({ color: 0xef4444, wireframe: true, transparent: true, opacity: 0.45 }));
    oct.position.set(1.4, 1.8, 0);
    scene.add(oct);
    const octIn = new THREE.Mesh(new THREE.OctahedronGeometry(0.32, 0), new THREE.MeshBasicMaterial({ color: 0x1a0000, transparent: true, opacity: 0.7 }));
    octIn.position.copy(oct.position);
    scene.add(octIn);
    objects.push({ mesh: oct, inner: octIn, tip: tips[2], speed: 0.012, axis: new THREE.Vector3(1, 0.5, 1).normalize(), base: oct.position.clone() });

    let mouse = { x: 0, y: 0 };
    let hoveredObj = null;
    const raycaster = new THREE.Raycaster();
    const mouseVec = new THREE.Vector2();

    const onMouseMove = e => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / W) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / H) * 2 + 1;
      mouseVec.set(mouse.x, mouse.y);
      raycaster.setFromCamera(mouseVec, camera);
      const hits = raycaster.intersectObjects(objects.map(o => o.mesh));
      const tip = tooltipRef.current;
      if (hits.length > 0) {
        const obj = objects.find(o => o.mesh === hits[0].object);
        if (obj && tip) {
          tip.style.display = "block";
          tip.innerHTML = obj.tip.replace("\n", "<br>");
          tip.style.left = (e.clientX + 14) + "px";
          tip.style.top = (e.clientY - 10) + "px";
          canvas.style.cursor = "pointer";
          hoveredObj = obj;
        }
      } else {
        if (tip) tip.style.display = "none";
        canvas.style.cursor = "default";
        hoveredObj = null;
      }
    };

    const onMouseLeave = () => {
      if (tooltipRef.current) tooltipRef.current.style.display = "none";
      hoveredObj = null;
    };

    const onClick = e => {
      const rect = canvas.getBoundingClientRect();
      mouseVec.set(((e.clientX - rect.left) / W) * 2 - 1, -((e.clientY - rect.top) / H) * 2 + 1);
      raycaster.setFromCamera(mouseVec, camera);
      const hits = raycaster.intersectObjects(objects.map(o => o.mesh));
      if (hits.length > 0) {
        const obj = objects.find(o => o.mesh === hits[0].object);
        if (obj) obj.burst = 0.15;
      }
    };

    canvas.addEventListener("mousemove", onMouseMove);
    canvas.addEventListener("mouseleave", onMouseLeave);
    canvas.addEventListener("click", onClick);

    let t = 0, animId;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      t += 0.016;
      objects.forEach((obj, i) => {
        const spd = obj.burst ? obj.speed * 8 : (hoveredObj === obj ? obj.speed * 2.5 : obj.speed);
        obj.mesh.rotateOnAxis(obj.axis, spd);
        if (obj.inner) obj.inner.rotateOnAxis(obj.axis, spd * 0.7);
        obj.mesh.position.y = obj.base.y + Math.sin(t * 0.7 + i * 1.2) * 0.12;
        if (obj.inner) obj.inner.position.y = obj.mesh.position.y;
        obj.mesh.position.x = obj.base.x + mouse.x * 0.12 * (i % 2 === 0 ? 1 : -1);
        if (obj.inner) obj.inner.position.x = obj.mesh.position.x;
        const ts = hoveredObj === obj ? 1.12 : 1;
        obj.mesh.scale.lerp(new THREE.Vector3(ts, ts, ts), 0.1);
        if (obj.inner) obj.inner.scale.copy(obj.mesh.scale);
        if (obj.burst) obj.burst = Math.max(0, obj.burst - 0.008);
      });
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(animId);
      canvas.removeEventListener("mousemove", onMouseMove);
      canvas.removeEventListener("mouseleave", onMouseLeave);
      canvas.removeEventListener("click", onClick);
      renderer.dispose();
    };
  }, []);

  return (
    <>
      <canvas ref={canvasRef} id="three-canvas" />
      <div ref={tooltipRef} className="tooltip3d" />
    </>
  );
}

// ── AUTH PAGE ──────────────────────────────────────────────
function AuthPage({ onLogin }) {
  const [tab, setTab] = useState("signin");
  const [users, setUsers] = useState({});
  const [form, setForm] = useState({ username: "", email: "", password: "", confirm: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const set = (k, v) => { setForm(f => ({ ...f, [k]: v })); setError(""); setSuccess(""); };

  const signin = () => {
    if (!form.username || !form.password) return setError("Fill in all fields.");
    const u = users[form.username];
    if (!u) return setError("Username not found.");
    if (u.password !== hashPw(form.password)) return setError("Wrong password.");
    onLogin(form.username);
  };

  const register = () => {
    if (!form.username || !form.email || !form.password || !form.confirm) return setError("Fill in all fields.");
    if (form.password !== form.confirm) return setError("Passwords don't match.");
    if (form.password.length < 6) return setError("Password too short (min 6).");
    if (users[form.username]) return setError("Username already taken.");
    setUsers(u => ({ ...u, [form.username]: { email: form.email, password: hashPw(form.password) } }));
    setSuccess("Account created — sign in now.");
    setTab("signin");
    setForm(f => ({ ...f, password: "", confirm: "" }));
  };

  return (
    <div className="auth-page">
      <ThreeHero />
      <div className="grid-bg" />
      <motion.div style={{ position: "relative", zIndex: 2, width: "100%", maxWidth: 440, display: "flex", flexDirection: "column", alignItems: "center" }}
        initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <div className="hero-tag" style={{ marginBottom: 24 }}>Deep Learning · Medical Imaging</div>
        <div className="hero-title" style={{ marginBottom: 12 }}>Detect<br /><span className="red">Lupus</span><br /><span className="dim">instantly.</span></div>
        <div className="hero-sub" style={{ marginBottom: 36 }}>Upload a dermoscopic image. Our YOLOv8 model classifies it in seconds.</div>

        <div className="auth-box">
          <div className="auth-tabs">
            <button className={`auth-tab ${tab === "signin" ? "active" : ""}`} onClick={() => { setTab("signin"); setError(""); setSuccess(""); }}>Sign in</button>
            <button className={`auth-tab ${tab === "register" ? "active" : ""}`} onClick={() => { setTab("register"); setError(""); setSuccess(""); }}>Create account</button>
          </div>

          {error && <div className="auth-error">{error}</div>}
          {success && <div className="auth-success">{success}</div>}

          {tab === "signin" ? (
            <>
              <div className="field"><label>Username</label><input placeholder="your username" value={form.username} onChange={e => set("username", e.target.value)} /></div>
              <div className="field"><label>Password</label><input type="password" placeholder="••••••••" value={form.password} onChange={e => set("password", e.target.value)} onKeyDown={e => e.key === "Enter" && signin()} /></div>
              <button className="auth-submit" onClick={signin}>Sign in</button>
            </>
          ) : (
            <>
              <div className="field"><label>Username</label><input placeholder="choose a username" value={form.username} onChange={e => set("username", e.target.value)} /></div>
              <div className="field"><label>Email</label><input placeholder="you@example.com" value={form.email} onChange={e => set("email", e.target.value)} /></div>
              <div className="field"><label>Password</label><input type="password" placeholder="min 6 chars" value={form.password} onChange={e => set("password", e.target.value)} /></div>
              <div className="field"><label>Confirm password</label><input type="password" placeholder="••••••••" value={form.confirm} onChange={e => set("confirm", e.target.value)} onKeyDown={e => e.key === "Enter" && register()} /></div>
              <button className="auth-submit" onClick={register}>Create account</button>
            </>
          )}
        </div>
        <div className="disclaimer" style={{ marginTop: 24, border: "none" }}>For educational and screening purposes only.<br />Not a substitute for professional medical diagnosis.</div>
      </motion.div>
    </div>
  );
}

// ── UPLOAD PAGE ────────────────────────────────────────────
function UploadPage({ user, onSignout, onResult }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [drag, setDrag] = useState(false);
  const inputRef = useRef(null);

  const handleFile = f => {
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
  };

  const analyze = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      const res = await fetch(`${API}/predict`, { method: "POST", body: fd });
      const data = await res.json();
      onResult(data, preview, file.name);
    } catch (e) {
      alert("Error connecting to backend. Make sure it's running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="app-header">
        <div className="app-logo">Lupus Detector</div>
        <div style={{ display: "flex", alignItems: "center" }}>
          <span className="app-user">Signed in as <strong style={{ color: "#fff" }}>{user}</strong></span>
          <button className="signout-btn" onClick={onSignout}>Sign out</button>
        </div>
      </div>

      <motion.div className="upload-page" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <div className="sec-tag">Step 01 — Upload</div>
        <div className="sec-title">Drop your<br />skin image here.</div>

        {!preview ? (
          <div className={`upload-zone ${drag ? "drag-over" : ""}`}
            onClick={() => inputRef.current.click()}
            onDragOver={e => { e.preventDefault(); setDrag(true); }}
            onDragLeave={() => setDrag(false)}
            onDrop={e => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files[0]); }}>
            <div className="upload-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="1.5">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" />
              </svg>
            </div>
            <div className="upload-text">Drag & drop or click to upload</div>
            <div className="upload-sub">PNG · JPG · JPEG · BMP · TIFF</div>
            <input ref={inputRef} type="file" className="upload-input" accept="image/*" onChange={e => handleFile(e.target.files[0])} />
          </div>
        ) : (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <img src={preview} alt="preview" className="preview-img" />
            <div className="img-meta">{file.name}</div>
            {loading ? (
              <div className="loading-overlay">
                <div className="spinner" />
                <div className="loading-text">Analyzing with YOLOv8...</div>
              </div>
            ) : (
              <>
                <button className="analyze-btn" onClick={analyze}>Analyze Image</button>
                <button className="reset-btn" onClick={() => { setFile(null); setPreview(null); }}>Choose different image</button>
              </>
            )}
          </motion.div>
        )}
      </motion.div>
      <div className="disclaimer">Medical disclaimer: For educational and screening purposes only.<br />Not a substitute for professional medical diagnosis.</div>
    </>
  );
}

// ── RESULTS PAGE ───────────────────────────────────────────
function ResultPage({ result, preview, filename, onReset }) {
  const isLupus = result.is_lupus;

  return (
    <>
      <div className="app-header">
        <div className="app-logo">Lupus Detector</div>
      </div>

      <motion.div className="result-page" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.45 }}>
        <div className="sec-tag">Step 02 — Results</div>
        <div className="sec-title">Analysis<br />complete.</div>

        <img src={preview} alt="analyzed" className="preview-img" style={{ marginBottom: 20 }} />

        <div className={`result-card ${isLupus ? "" : "safe"}`}>
          <div className={`result-badge ${isLupus ? "" : "safe"}`}>
            {isLupus ? "⚠ Positive detection" : "✓ Negative — no lupus"}
          </div>
          <div className="result-heading">{isLupus ? "Lupus Detected" : "No Lupus Detected"}</div>
          <div className="result-meta">Confidence: {result.confidence}% · {result.analyzed_at}</div>

          <div className="bar-wrap">
            {result.breakdown.map((b, i) => (
              <div key={i} className="bar-row">
                <span className="bar-name">{b.name}</span>
                <div className="bar-track">
                  <motion.div className={`bar-fill ${b.name.toUpperCase() === "LUPUS" ? (isLupus ? "lupus" : "dim") : (isLupus ? "dim" : "safe")}`}
                    initial={{ width: 0 }} animate={{ width: `${b.probability}%` }} transition={{ duration: 1.2, ease: [0.25, 0.8, 0.25, 1] }} />
                </div>
                <span className="bar-pct">{b.probability}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="details-grid">
          <div className="d-cell"><div className="d-key">Predicted class</div><div className="d-val">{result.label}</div></div>
          <div className="d-cell"><div className="d-key">Model</div><div className="d-val">{result.model}</div></div>
          <div className="d-cell"><div className="d-key">Image size</div><div className="d-val">{result.image_size} px</div></div>
          <div className="d-cell"><div className="d-key">Analyzed at</div><div className="d-val">{result.analyzed_at}</div></div>
        </div>

        {isLupus && (
          <div style={{ marginTop: 20, padding: "16px 20px", border: "1px solid rgba(239,68,68,0.15)", background: "rgba(239,68,68,0.03)", fontSize: 12, color: "rgba(255,255,255,0.4)", lineHeight: 1.7 }}>
            Please consult a dermatologist or rheumatologist for a proper clinical diagnosis.
          </div>
        )}

        <button className="analyze-again-btn" onClick={onReset}>Analyze another image</button>
      </motion.div>
      <div className="disclaimer">Medical disclaimer: For educational and screening purposes only.<br />Not a substitute for professional medical diagnosis.</div>
    </>
  );
}

// ── APP ROOT ───────────────────────────────────────────────
export default function App() {
  const [user, setUser] = useState(null);
  const [result, setResult] = useState(null);
  const [preview, setPreview] = useState(null);
  const [filename, setFilename] = useState(null);

  const handleResult = (data, prev, name) => {
    setResult(data);
    setPreview(prev);
    setFilename(name);
  };

  const reset = () => { setResult(null); setPreview(null); setFilename(null); };
  const signout = () => { setUser(null); reset(); };

  if (!user) return <AuthPage onLogin={setUser} />;
  if (result) return <ResultPage result={result} preview={preview} filename={filename} onReset={reset} />;
  return <UploadPage user={user} onSignout={signout} onResult={handleResult} />;
}