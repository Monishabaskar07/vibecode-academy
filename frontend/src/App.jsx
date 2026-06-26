import React, { useState, useEffect, useRef } from 'react';

function App() {
  // --- UI & Controls State ---
  const [prompt, setPrompt] = useState('Create a binary search tree with values 15, 10, 20, 8, 12, 17, 25, then insert 12');
  const [eli5Mode, setEli5Mode] = useState(false);
  const [audioNarrate, setAudioNarrate] = useState(false);
  const [raceMode, setRaceMode] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // --- Multi-Agent Session Payload ---
  const [sessionData, setSessionData] = useState(null);
  const [agentLogs, setAgentLogs] = useState([
    { source: 'system', text: 'System Online. Enter a verbal instruction to design your algorithm.' }
  ]);

  // --- Traversal & Animation State ---
  const [activeStep, setActiveStep] = useState(-1);
  const [isPlaying, setIsPlaying] = useState(false);
  const animationTimer = useRef(null);

  // --- Gamification (Race Mode & Quiz) ---
  const [score, setScore] = useState(0);
  const [quizActive, setQuizActive] = useState(false);
  const [selectedQuizAnswer, setSelectedQuizAnswer] = useState(null);
  const [quizCompleted, setQuizCompleted] = useState(false);

  // --- Cryptographic Vault State ---
  const [vaultPasscode, setVaultPasscode] = useState('');
  const [vaultStatus, setVaultStatus] = useState({ exists: false, is_locked: true });
  const [vaultDecryptedData, setVaultDecryptedData] = useState(null);
  const [vaultError, setVaultError] = useState('');
  const [vaultForm, setVaultForm] = useState({
    studentName: 'Moniii',
    gradeLevel: 'College Sophomore',
    homeworkNotes: 'Struggled with tree rotations in assignment 3, but mastered BST insertions!',
    gradesSummary: 'A- (Data Structures Lab)'
  });

  // --- Performance Benchmarks State ---
  const [benchmarks, setBenchmarks] = useState([]);
  const [benchRunning, setBenchRunning] = useState(false);

  // --- API Base URL ---
  const API_BASE = 'http://127.0.0.1:8000/api';

  // --- Fetch Initial Data ---
  useEffect(() => {
    fetchVaultStatus();
    fetchBenchmarks();
  }, []);

  const fetchVaultStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/vault/status`);
      const data = await res.json();
      setVaultStatus(data);
    } catch (err) {
      console.error('Error fetching vault status:', err);
    }
  };

  const fetchBenchmarks = async () => {
    try {
      const res = await fetch(`${API_BASE}/benchmarks`);
      const data = await res.json();
      setBenchmarks(data);
    } catch (err) {
      console.error('Error fetching benchmarks:', err);
    }
  };

  // --- Browser Text-to-Speech (TTS) Narrator ---
  const speakText = (text) => {
    if ('speechSynthesis' in window && audioNarrate) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95;
      utterance.pitch = 1.1; // Cool, slightly high futuristic voice
      window.speechSynthesis.speak(utterance);
    }
  };

  // --- Agent Pipeline Trigger ---
  const handleRunSession = async (e) => {
    if (e) e.preventDefault();
    if (!prompt.trim()) return;

    setIsLoading(true);
    setIsPlaying(false);
    setActiveStep(-1);
    if (animationTimer.current) clearInterval(animationTimer.current);

    // Initial log
    setAgentLogs([
      { source: 'security', text: '🔍 Security Guard: Intercepted prompt. Scanning for sensitive child PII & intellectual property...' }
    ]);

    try {
      const res = await fetch(`${API_BASE}/session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, eli5_mode: eli5Mode })
      });
      const data = await res.json();

      setSessionData(data);
      
      // Build step-by-step log narrative
      const newLogs = [
        { source: 'security', text: `🛡️ Security Guard: Prompt sanitization complete. Redacted student credentials. Cleaned prompt: "${data.security.sanitized_prompt}"` },
        { source: 'architect', text: `📐 Architect: Parsed verbal commands. Generated spatial coordinates for ${data.values.length} nodes.` },
        { source: 'chaos', text: `⚡ Chaos Agent: Running stress test at level [${data.chaos.level}]. Injected edge-case challenge!` },
        { source: 'coordinator', text: `🎓 Coordinator: Multi-agent compilation successful. Animating data structure operations.` }
      ];
      setAgentLogs(prev => [...prev, ...newLogs]);

      // Auto play animation
      setIsPlaying(true);
      setActiveStep(0);
    } catch (err) {
      setAgentLogs(prev => [...prev, { source: 'chaos', text: '❌ Error executing multi-agent pipeline. Backend server offline.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  // --- Animation Stepper ---
  useEffect(() => {
    if (!isPlaying || !sessionData || sessionData.trace.length === 0) return;

    // Trigger voice narration for the current step
    const currentTrace = sessionData.trace[activeStep];
    if (currentTrace) {
      const textToSpeak = eli5Mode ? currentTrace.metaphor : currentTrace.explanation;
      speakText(textToSpeak);
    }

    animationTimer.current = setTimeout(() => {
      if (activeStep < sessionData.trace.length - 1) {
        setActiveStep(prev => prev + 1);
      } else {
        setIsPlaying(false);
        // Prompt quiz at the end of the session
        setQuizActive(true);
        setSelectedQuizAnswer(null);
        setQuizCompleted(false);
        setAgentLogs(prev => [...prev, { source: 'coordinator', text: '🎉 Session complete. Generating active recall academic quiz.' }]);
      }
    }, 4500); // 4.5 seconds per node step to allow TTS narration

    return () => clearTimeout(animationTimer.current);
  }, [isPlaying, activeStep, sessionData]);

  // --- Interactive Canvas Guessing (Race Mode) ---
  const handleNodeClick = (nodeVal) => {
    if (!raceMode || !isPlaying || !sessionData) return;
    
    const currentTrace = sessionData.trace[activeStep];
    if (!currentTrace) return;

    const nextInsertedVal = currentTrace.value;
    if (nodeVal === nextInsertedVal) {
      setScore(prev => prev + 10);
      setAgentLogs(prev => [...prev, { source: 'coordinator', text: `🎯 Correct! You predicted the next traversal node: ${nodeVal}. (+10 points)` }]);
    } else {
      setAgentLogs(prev => [...prev, { source: 'chaos', text: `❌ Incorrect. You guessed node ${nodeVal}, but the tree inserted node ${nextInsertedVal} next.` }]);
    }
  };

  // --- Vault Cryptographic Actions ---
  const handleSaveVault = async (e) => {
    e.preventDefault();
    setVaultError('');
    try {
      const res = await fetch(`${API_BASE}/vault/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          passcode: vaultPasscode,
          student_name: vaultForm.studentName,
          grade_level: vaultForm.gradeLevel,
          homework_notes: vaultForm.homeworkNotes,
          grades_summary: vaultForm.gradesSummary
        })
      });
      const data = await res.json();
      fetchVaultStatus();
      setVaultPasscode('');
      setAgentLogs(prev => [...prev, { source: 'security', text: '🔒 Security Guard: Profile details encrypted locally using AES-256-GCM.' }]);
    } catch (err) {
      setVaultError('Failed to save vault data.');
    }
  };

  const handleUnlockVault = async (e) => {
    e.preventDefault();
    setVaultError('');
    if (!vaultPasscode) {
      setVaultError('Enter passcode to decrypt.');
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/vault/unlock`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ passcode: vaultPasscode })
      });
      
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Decryption failed.');
      }

      const data = await res.json();
      setVaultDecryptedData(data);
      setVaultStatus(prev => ({ ...prev, is_locked: false }));
      setAgentLogs(prev => [...prev, { source: 'security', text: '🔓 Security Guard: Cryptographic vault key matches. Decrypted student profile.' }]);
    } catch (err) {
      setVaultError(err.message);
    }
  };

  const handleLockVault = async () => {
    try {
      await fetch(`${API_BASE}/vault/lock`, { method: 'POST' });
      setVaultDecryptedData(null);
      setVaultStatus(prev => ({ ...prev, is_locked: true }));
      setVaultPasscode('');
      setAgentLogs(prev => [...prev, { source: 'security', text: '🔒 Security Guard: Cryptographic vault locked. Memory cleared.' }]);
    } catch (err) {
      console.error(err);
    }
  };

  // --- Run Benchmarks ---
  const handleRunBenchmark = async (algorithm, numOps) => {
    setBenchRunning(true);
    setAgentLogs(prev => [...prev, { source: 'coordinator', text: `📊 Benchmark: Requesting custom MCP Server to run ${numOps} operations for ${algorithm.toUpperCase()}...` }]);
    try {
      const res = await fetch(`${API_BASE}/benchmarks/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithm, num_operations: numOps })
      });
      const data = await res.json();
      fetchBenchmarks();
      setAgentLogs(prev => [...prev, { source: 'coordinator', text: `📈 Benchmark Results: Placed ${numOps} elements in ${data.time_taken_ms} ms. Complexity: ${data.complexity}` }]);
    } catch (err) {
      console.error(err);
    } finally {
      setBenchRunning(false);
    }
  };

  // --- Quiz Submission ---
  const handleQuizAnswer = async (idx) => {
    if (quizCompleted) return;
    setSelectedQuizAnswer(idx);
    setQuizCompleted(true);
    
    const isCorrect = idx === sessionData.chaos.quiz_question.answer_idx;
    if (isCorrect) {
      setScore(prev => prev + 50);
      setAgentLogs(prev => [...prev, { source: 'coordinator', text: '🎓 Quiz Complete: Correct! Earned +50 points. Local progress recorded.' }]);
      
      // Log progress to SQLite challenges table
      try {
        await fetch(`${API_BASE}/challenges/update`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            challenge_name: "Binary Search Tree Basics",
            status: "Completed",
            score: score + 50
          })
        });
      } catch (e) {
        console.error(e);
      }
    } else {
      setAgentLogs(prev => [...prev, { source: 'chaos', text: '🎓 Quiz Complete: Incorrect. Review the explanation in the quiz panel.' }]);
    }
  };

  // --- Node Visited Helper ---
  const isNodeVisited = (nodeId) => {
    if (!sessionData || activeStep === -1) return false;
    const currentTrace = sessionData.trace[activeStep];
    return currentTrace ? currentTrace.visited.includes(nodeId) : false;
  };

  const isNodeJustInserted = (nodeId) => {
    if (!sessionData || activeStep === -1) return false;
    const currentTrace = sessionData.trace[activeStep];
    return currentTrace ? currentTrace.node_id === nodeId : false;
  };

  return (
    <div className="app-container">
      {/* HEADER BAR */}
      <header>
        <div className="logo-section">
          <div className="logo-icon">V</div>
          <div className="logo-title">
            <h1>VibeCode Academy</h1>
            <div className="logo-subtitle">Multi-Agent DSA Playpen</div>
          </div>
        </div>
        
        {/* GAME HUD */}
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255,255,255,0.03)', padding: '0.4rem 0.8rem', borderRadius: '6px', border: '1px solid var(--glass-border)' }}>
            <span style={{ fontSize: '0.7rem', color: 'hsl(var(--text-muted))', textTransform: 'uppercase' }}>Session Score</span>
            <span style={{ fontSize: '1.1rem', fontWeight: 700, color: 'hsl(var(--accent-green))', fontFamily: 'var(--font-mono)' }}>{score} pts</span>
          </div>
          <button className="btn-sec" onClick={() => handleRunSession(null)}>
            🔄 Reset Canvas
          </button>
        </div>
      </header>

      {/* DASHBOARD CORE */}
      <div className="dashboard-grid">
        
        {/* LEFT PANEL: CHAT & AGENT LOGS */}
        <div className="sidebar-panel">
          {/* Chat Interface */}
          <div className="chat-section">
            <div className="chat-bubble agent">
              <strong>🎓 Coordinator Agent</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '0.25rem' }}>
                Welcome! Describe an algorithm (like a Binary Search Tree or AVL Tree) with a list of values. I will coordinate our agent team to build, animate, and stress-test it for you.
              </p>
            </div>

            {sessionData && (
              <div className="chat-bubble user">
                <p style={{ fontSize: '0.9rem' }}>{sessionData.security.raw_prompt}</p>
              </div>
            )}

            {sessionData && (
              <div className="chat-bubble agent">
                <strong>🎓 Coordinator Agent</strong>
                <p style={{ fontSize: '0.9rem', marginTop: '0.25rem' }}>
                  {sessionData.summary}
                </p>
              </div>
            )}
          </div>

          {/* Agent Thought Logs Console */}
          <div className="agent-logs-container">
            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'hsl(var(--text-muted))', marginBottom: '0.5rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.25rem' }}>
              📟 Agent Thought Logs (ADK Trace)
            </div>
            {agentLogs.map((log, i) => (
              <div key={i} className={`log-entry ${log.source}`}>
                {log.text}
              </div>
            ))}
          </div>

          {/* Secure Academic Vault Panel */}
          <div className="vault-panel">
            <div className="vault-header">
              <span className={`vault-status-indicator ${vaultStatus.is_locked ? 'locked' : 'unlocked'}`}></span>
              <span>🔐 Student Academic Vault (AES-256-GCM)</span>
            </div>
            
            {vaultStatus.is_locked ? (
              <form onSubmit={handleUnlockVault} className="vault-credentials-row">
                <input 
                  type="password" 
                  placeholder="Enter Vault Passcode" 
                  value={vaultPasscode}
                  onChange={e => setVaultPasscode(e.target.value)}
                />
                <button type="submit" className="btn-sec" style={{ borderColor: 'hsl(var(--accent-purple))' }}>Unlock</button>
              </form>
            ) : (
              <div>
                <div className="vault-display">
                  <strong>Unlocked Profile:</strong><br />
                  {vaultDecryptedData?.profile}<br />
                  <strong>Academic Record:</strong> {vaultDecryptedData?.grades}
                </div>
                <button onClick={handleLockVault} className="btn-sec" style={{ marginTop: '0.5rem', width: '100%', borderColor: 'hsl(var(--accent-red))', color: 'hsl(var(--accent-red))' }}>
                  Lock Vault
                </button>
              </div>
            )}

            {vaultStatus.is_locked && !vaultStatus.exists && (
              <form onSubmit={handleSaveVault} style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', background: 'rgba(0,0,0,0.15)', padding: '0.5rem', borderRadius: '6px' }}>
                <span style={{ fontSize: '0.7rem', color: 'hsl(var(--text-muted))' }}>Create Secure Profile:</span>
                <input 
                  type="text" 
                  placeholder="Passcode" 
                  value={vaultPasscode} 
                  onChange={e => setVaultPasscode(e.target.value)} 
                  style={{ background: '#000', border: '1px solid var(--glass-border)', borderRadius: '4px', padding: '0.25rem', color: '#fff', fontSize: '0.75rem' }}
                />
                <button type="submit" className="btn-sec" style={{ fontSize: '0.75rem', padding: '0.25rem' }}>Save & Lock</button>
              </form>
            )}

            {vaultError && <div style={{ fontSize: '0.7rem', color: 'hsl(var(--accent-red))', fontFamily: 'var(--font-mono)' }}>⚠️ {vaultError}</div>}
          </div>

          {/* Interactive Chat Input Console */}
          <form onSubmit={handleRunSession} className="chat-input-area">
            <div className="input-row">
              <input 
                type="text" 
                value={prompt}
                onChange={e => setPrompt(e.target.value)}
                placeholder="Describe your data structure operation..."
                disabled={isLoading}
              />
              <button type="submit" className="btn" disabled={isLoading}>
                {isLoading ? 'Processing...' : 'Deploy'}
              </button>
            </div>
            
            {/* Toggles */}
            <div className="toggle-controls">
              <label className="toggle-item">
                <input 
                  type="checkbox" 
                  checked={eli5Mode}
                  onChange={e => setEli5Mode(e.target.checked)}
                />
                <span>💡 ELI5 Metaphors</span>
              </label>
              
              <label className="toggle-item">
                <input 
                  type="checkbox" 
                  checked={audioNarrate}
                  onChange={e => setAudioNarrate(e.target.checked)}
                />
                <span>🔊 Voice Narrate</span>
              </label>

              <label className="toggle-item">
                <input 
                  type="checkbox" 
                  checked={raceMode}
                  onChange={e => setRaceMode(e.target.checked)}
                />
                <span style={{ color: raceMode ? 'hsl(var(--accent-green))' : '' }}>🎮 Race Mode</span>
              </label>
            </div>
          </form>
        </div>

        {/* RIGHT AREA: VISUAL CANVAS & PERFORMANCE STATS */}
        <div className="main-workspace">
          
          {/* TOP AREA: INTERACTIVE VISUAL CANVAS */}
          <div className="canvas-container">
            {raceMode && isPlaying && (
              <div className="game-overlay">
                ⚡ <strong>Race the Agent!</strong> Click the node on the canvas you think the search path will visit next!
              </div>
            )}

            {/* SVG Tree Drawer */}
            {sessionData ? (
              <svg className="canvas-svg">
                {/* Draw Edges */}
                {sessionData.nodes.map(node => {
                  const edges = [];
                  if (node.left) {
                    const child = sessionData.nodes.find(n => n.id === node.left);
                    if (child) {
                      edges.push(
                        <line 
                          key={`${node.id}-${child.id}`}
                          x1={node.x} y1={node.y}
                          x2={child.x} y2={child.y}
                          className="tree-edge"
                        />
                      );
                    }
                  }
                  if (node.right) {
                    const child = sessionData.nodes.find(n => n.id === node.right);
                    if (child) {
                      edges.push(
                        <line 
                          key={`${node.id}-${child.id}`}
                          x1={node.x} y1={node.y}
                          x2={child.x} y2={child.y}
                          className="tree-edge"
                        />
                      );
                    }
                  }
                  return edges;
                })}

                {/* Draw Nodes */}
                {sessionData.nodes.map(node => {
                  const visited = isNodeVisited(node.id);
                  const active = isNodeJustInserted(node.id);
                  let nodeClass = "";
                  if (visited) nodeClass = "node-visited";
                  if (active) nodeClass = "node-active-insert";

                  return (
                    <g 
                      key={node.id} 
                      transform={`translate(0, 0)`}
                      className={`tree-node ${nodeClass}`}
                      onClick={() => handleNodeClick(node.value)}
                    >
                      <circle 
                        cx={node.x} cy={node.y} r="22" 
                        className="tree-node-circle"
                      />
                      <text cx={node.x} cy={node.y} className="tree-node-text" x={node.x} y={node.y}>
                        {node.value}
                      </text>
                    </g>
                  );
                })}
              </svg>
            ) : (
              <div style={{ textAlign: 'center', color: 'hsl(var(--text-muted))' }}>
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" style={{ color: 'hsla(var(--accent-cyan), 0.3)', marginBottom: '1rem' }}>
                  <circle cx="12" cy="5" r="3" />
                  <circle cx="5" cy="19" r="3" />
                  <circle cx="19" cy="19" r="3" />
                  <path d="M12 8v8M5 16l7-8 7 8" />
                </svg>
                <p>Verify configurations and click <strong>Deploy</strong> to load the visual algorithm canvas.</p>
              </div>
            )}

            {/* Active Step Narration Banner */}
            {sessionData && activeStep !== -1 && (
              <div style={{ position: 'absolute', bottom: '1rem', left: '1rem', right: '1rem', background: 'hsla(var(--bg-panel-light), 0.85)', backdropFilter: 'blur(8px)', borderLeft: '4px solid hsl(var(--accent-cyan))', padding: '0.75rem 1.25rem', borderRadius: '4px', fontSize: '0.9rem' }}>
                <strong>Step {activeStep + 1}/{sessionData.trace.length}:</strong>{' '}
                {eli5Mode ? sessionData.trace[activeStep].metaphor : sessionData.trace[activeStep].explanation}
              </div>
            )}

            {/* Automated Quiz Overlay */}
            {quizActive && sessionData && (
              <div className="quiz-overlay">
                <div className="quiz-card">
                  <div className="quiz-title">🎓 Active Recall Academic Quiz</div>
                  <div className="quiz-question-text">
                    <strong>Question:</strong> {sessionData.chaos.quiz_question.question}
                  </div>
                  
                  <div className="quiz-options">
                    {sessionData.chaos.quiz_question.options.map((opt, idx) => {
                      let btnClass = "";
                      if (quizCompleted) {
                        if (idx === sessionData.chaos.quiz_question.answer_idx) btnClass = "correct";
                        else if (idx === selectedQuizAnswer) btnClass = "wrong";
                      }
                      return (
                        <button 
                          key={idx}
                          className={`quiz-option-btn ${btnClass}`}
                          onClick={() => handleQuizAnswer(idx)}
                          disabled={quizCompleted}
                        >
                          {opt}
                        </button>
                      );
                    })}
                  </div>

                  {quizCompleted && (
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '0.75rem', borderRadius: '8px', fontSize: '0.85rem', border: '1px solid var(--glass-border)', marginBottom: '1.5rem' }}>
                      <strong>Explanation:</strong> {sessionData.chaos.quiz_question.explanation}
                    </div>
                  )}

                  <button className="btn" style={{ width: '100%' }} onClick={() => setQuizActive(false)}>
                    Close Quiz Room
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* LOWER AREA: PERFORMANCE STATS & LIVE SECURITY COMPARISON */}
          <div className="lower-panel">
            
            {/* Performance Stats & Benchmarks */}
            <div className="stats-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#fff' }}>📊 Performance Benchmarks (MCP Link)</span>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button className="btn-sec" style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }} onClick={() => handleRunBenchmark('bst', 5000)} disabled={benchRunning}>
                    Bench BST
                  </button>
                  <button className="btn-sec" style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }} onClick={() => handleRunBenchmark('avl', 5000)} disabled={benchRunning}>
                    Bench AVL
                  </button>
                </div>
              </div>

              <div className="stats-grid">
                <div className="metric-box">
                  <div className="metric-label">Complexity</div>
                  <div className="metric-value">O(log N)</div>
                </div>
                <div className="metric-box">
                  <div className="metric-label">Active Nodes</div>
                  <div className="metric-value">{sessionData ? sessionData.values.length : 0}</div>
                </div>
                <div className="metric-box">
                  <div className="metric-label">Bench Time</div>
                  <div className="metric-value" style={{ color: 'hsl(var(--accent-amber))' }}>
                    {benchmarks.length > 0 ? `${benchmarks[0].time_taken_ms} ms` : '0.0 ms'}
                  </div>
                </div>
              </div>

              {/* Benchmarks Logs */}
              <div style={{ flex: 1, overflowY: 'auto', marginTop: '0.75rem', fontSize: '0.7rem', color: 'hsl(var(--text-muted))', fontFamily: 'var(--font-mono)' }}>
                <div style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.25rem', marginBottom: '0.25rem' }}>Historical Benchmarks:</div>
                {benchmarks.map((b, idx) => (
                  <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.1rem 0' }}>
                    <span>{b.algorithm.toUpperCase()} (N={b.num_operations})</span>
                    <span style={{ color: 'hsl(var(--accent-cyan))' }}>{b.time_taken_ms} ms</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Live Privacy & IP Guard Panel */}
            <div className="privacy-guard-card">
              <div className="privacy-header">
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#fff' }}>🛡️ PII & IP Sanitization Guard</span>
                <span className="privacy-badge">Guarded: AES-256</span>
              </div>

              <div className="privacy-comparison-grid">
                <div>
                  <div style={{ color: 'hsl(var(--accent-red))', marginBottom: '0.25rem', fontSize: '0.65rem', textTransform: 'uppercase' }}>Raw Prompt (Local)</div>
                  <div className="prompt-box">
                    {sessionData ? sessionData.security.raw_prompt : "No active session."}
                  </div>
                </div>
                <div>
                  <div style={{ color: 'hsl(var(--accent-green))', marginBottom: '0.25rem', fontSize: '0.65rem', textTransform: 'uppercase' }}>Sanitized Outbound</div>
                  <div className="prompt-box redacted">
                    {sessionData ? sessionData.security.sanitized_prompt : "No active session."}
                  </div>
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}

export default App;
