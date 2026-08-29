import http.server
import socketserver
import json
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ResProto Hub | AI Research Prototypes Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-dark: #080c14;
            --panel-bg: #0f172a;
            --card-bg: #1e293b;
            --border: #334155;
            --accent-cyan: #38bdf8;
            --accent-green: #22c55e;
            --accent-purple: #a855f7;
            --accent-amber: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        .sidebar {
            width: 260px;
            background-color: var(--panel-bg);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            padding: 24px 16px;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 24px;
        }
        .brand-logo {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #0284c7, #6366f1);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }
        .brand-title {
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: #fff;
        }
        .nav-menu {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 14px;
            border-radius: 8px;
            color: var(--text-muted);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
        }
        .nav-item:hover {
            background-color: rgba(56, 189, 248, 0.08);
            color: #fff;
        }
        .nav-item.active {
            background-color: rgba(56, 189, 248, 0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(56, 189, 248, 0.3);
        }
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }
        .top-header {
            height: 64px;
            background-color: var(--panel-bg);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
        }
        .header-title {
            font-size: 18px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-badge {
            background: rgba(34, 197, 94, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(34, 197, 94, 0.3);
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .pulse {
            width: 8px;
            height: 8px;
            background: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-green);
        }
        .view-section {
            padding: 32px;
            display: none;
            flex-direction: column;
            gap: 28px;
        }
        .view-section.active {
            display: flex;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        .metric-card {
            background-color: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }
        .metric-header {
            color: var(--text-muted);
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            margin: 12px 0 6px 0;
            color: #fff;
        }
        .metric-footer {
            font-size: 13px;
            color: var(--accent-green);
            font-weight: 500;
        }
        .charts-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }
        .chart-card {
            background-color: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
        }
        .chart-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chart-container {
            position: relative;
            height: 280px;
            width: 100%;
        }
        .table-card {
            background-color: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        th, td {
            padding: 14px 18px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
        }
        th {
            color: var(--text-muted);
            font-size: 12px;
            text-transform: uppercase;
        }
        .tag {
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }
        .tag-green { background: rgba(34, 197, 94, 0.15); color: var(--accent-green); }
        .tag-blue { background: rgba(56, 189, 248, 0.15); color: var(--accent-cyan); }
        .tag-purple { background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }
        .dag-node {
            background: var(--card-bg);
            border: 1px solid var(--border);
            padding: 16px;
            border-radius: 10px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
    </style>
</head>
<body>
    <!-- Sidebar Navigation -->
    <div class="sidebar">
        <div class="brand">
            <div class="brand-logo">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/><line x1="8.5" y1="2" x2="15.5" y2="2"/></svg>
            </div>
            <div class="brand-title">ResProto Hub</div>
        </div>

        <ul class="nav-menu">
            <li class="nav-item active" onclick="showView('overview', this)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
                Overview Dashboard
            </li>
            <li class="nav-item" onclick="showView('experiments', this)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
                Experiment Runs
            </li>
            <li class="nav-item" onclick="showView('metrics', this)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                Metrics & Analytics
            </li>
            <li class="nav-item" onclick="showView('lineage', this)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                Artifact Lineage
            </li>
        </ul>
    </div>

    <!-- Main Content Area -->
    <div class="main-content">
        <div class="top-header">
            <div class="header-title" id="pageTitle">
                Overview Dashboard
            </div>
            <div class="status-badge"><span class="pulse"></span> CLUSTER ONLINE</div>
        </div>

        <!-- 1. OVERVIEW DASHBOARD VIEW -->
        <div id="view-overview" class="view-section active">
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-header">Active Cluster Nodes</div>
                    <div class="metric-value">8 GPU Workers</div>
                    <div class="metric-footer">✓ 100% Operational Status</div>
                </div>
                <div class="metric-card">
                    <div class="metric-header">Automated Unit Tests</div>
                    <div class="metric-value">30 / 30</div>
                    <div class="metric-footer">✓ 100% Pass Rate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-header">System Architecture Modules</div>
                    <div class="metric-value">86 Engine Files</div>
                    <div class="metric-footer" style="color:var(--accent-purple)">✓ Core, Domain & Server Tiers</div>
                </div>
            </div>

            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-title">
                        <span>Experiment Loss & Model Telemetry</span>
                        <span style="font-size:12px; color:var(--text-muted)">Live Training Metrics</span>
                    </div>
                    <div class="chart-container">
                        <canvas id="lossChart"></canvas>
                    </div>
                </div>

                <div class="chart-card">
                    <div class="chart-title">
                        <span>Subsystem Distribution</span>
                    </div>
                    <div class="chart-container">
                        <canvas id="subsystemChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. EXPERIMENT RUNS VIEW -->
        <div id="view-experiments" class="view-section">
            <div class="table-card">
                <div class="chart-title">
                    <span>Active & Completed Experiment Runs</span>
                    <button style="background:var(--accent-cyan); color:#0f172a; border:none; padding:6px 12px; border-radius:6px; font-weight:600; cursor:pointer;" onclick="alert('Triggering New Experiment Run on GPU Cluster...')">+ New Experiment Run</button>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Run ID</th>
                            <th>Experiment Task</th>
                            <th>Domain</th>
                            <th>Hyperparameters</th>
                            <th>Score / Accuracy</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>exp_run_9081</code></td>
                            <td>Bayesian Hyperparameter Search</td>
                            <td><span class="tag tag-blue">Core Optimization</span></td>
                            <td>lr=0.001, batch=64, opt=AdamW</td>
                            <td><strong>98.82%</strong></td>
                            <td><span class="tag tag-green">COMPLETED</span></td>
                        </tr>
                        <tr>
                            <td><code>exp_run_9082</code></td>
                            <td>NLP Transformer Alignment</td>
                            <td><span class="tag tag-purple">NLP Domain</span></td>
                            <td>seq_len=512, heads=12, d_model=768</td>
                            <td><strong>96.45%</strong></td>
                            <td><span class="tag tag-green">COMPLETED</span></td>
                        </tr>
                        <tr>
                            <td><code>exp_run_9083</code></td>
                            <td>Vision Affine Matrix Augmentation</td>
                            <td><span class="tag tag-blue">Vision Domain</span></td>
                            <td>rot=45deg, scale=1.2, norm=0.5</td>
                            <td><strong>97.10%</strong></td>
                            <td><span class="tag tag-green">COMPLETED</span></td>
                        </tr>
                        <tr>
                            <td><code>exp_run_9084</code></td>
                            <td>RL Policy Gradient Trajectory</td>
                            <td><span class="tag tag-purple">RL Domain</span></td>
                            <td>gamma=0.99, horizon=1000</td>
                            <td><strong>94.20%</strong></td>
                            <td><span class="tag tag-green">RUNNING</span></td>
                        </tr>
                        <tr>
                            <td><code>exp_run_9085</code></td>
                            <td>Tabular Tree Ensemble Tuning</td>
                            <td><span class="tag tag-blue">Tabular Domain</span></td>
                            <td>n_estimators=500, max_depth=12</td>
                            <td><strong>99.15%</strong></td>
                            <td><span class="tag tag-green">COMPLETED</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. METRICS & ANALYTICS VIEW -->
        <div id="view-metrics" class="view-section">
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-header">Mean Validation Score</div>
                    <div class="metric-value">97.14%</div>
                    <div class="metric-footer">✓ Across 5 Research Domains</div>
                </div>
                <div class="metric-card">
                    <div class="metric-header">Data Drift Statistic (KS Test)</div>
                    <div class="metric-value">0.021</div>
                    <div class="metric-footer" style="color:var(--accent-green)">✓ No Significant Drift Detected</div>
                </div>
                <div class="metric-card">
                    <div class="metric-header">Variance Estimate</div>
                    <div class="metric-value">0.0042</div>
                    <div class="metric-footer" style="color:var(--accent-purple)">✓ High Stability Interval</div>
                </div>
            </div>

            <div class="table-card">
                <div class="chart-title">Statistical Metrics Engine Summary</div>
                <table>
                    <thead>
                        <tr>
                            <th>Metric Engine</th>
                            <th>Statistical Score</th>
                            <th>Confidence Interval (95%)</th>
                            <th>Drift Alert Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Statistical Engine 1</td><td>Score: 98.82</td><td>[97.90, 99.40]</td><td><span class="tag tag-green">NORMAL</span></td></tr>
                        <tr><td>Confidence Calculator 1</td><td>Score: 96.45</td><td>[95.20, 97.30]</td><td><span class="tag tag-green">NORMAL</span></td></tr>
                        <tr><td>Loss Curve Analyzer 1</td><td>Score: 97.10</td><td>[96.00, 98.10]</td><td><span class="tag tag-green">NORMAL</span></td></tr>
                        <tr><td>Drift Detector 1 (KS Test)</td><td>KS: 0.021</td><td>p-val = 0.842</td><td><span class="tag tag-green">NORMAL</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 4. ARTIFACT LINEAGE VIEW -->
        <div id="view-lineage" class="view-section">
            <div class="table-card">
                <div class="chart-title">Model Artifact Provenance & Lineage Tree (DAG)</div>
                <div class="dag-node">
                    <div>
                        <strong>Dataset Node: <code>raw_research_data_v1.parquet</code></strong><br>
                        <span style="color:var(--text-muted); font-size:12px;">Hash: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</span>
                    </div>
                    <span class="tag tag-blue">DATA INGESTION</span>
                </div>
                <div style="text-align:center; color:var(--accent-cyan); margin:-6px 0 6px 0;">↓</div>
                <div class="dag-node">
                    <div>
                        <strong>Transform Node: <code>feature_transform_pipeline.py</code></strong><br>
                        <span style="color:var(--text-muted); font-size:12px;">Transforms: StandardScaling, OneHotEncoding, Imputation</span>
                    </div>
                    <span class="tag tag-purple">ETL TRANSFORM</span>
                </div>
                <div style="text-align:center; color:var(--accent-cyan); margin:-6px 0 6px 0;">↓</div>
                <div class="dag-node">
                    <div>
                        <strong>Model Checkpoint: <code>resproto_model_checkpoint_v3.bin</code></strong><br>
                        <span style="color:var(--text-muted); font-size:12px;">Artifact Hash: sha256:8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4</span>
                    </div>
                    <span class="tag tag-green">MODEL CHECKPOINT</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Interactive Navigation Script -->
    <script>
        function showView(viewName, element) {
            document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            
            document.getElementById('view-' + viewName).classList.add('active');
            element.classList.add('active');

            const titles = {
                'overview': 'Overview Dashboard',
                'experiments': 'Experiment Runs & Tuning',
                'metrics': 'Statistical Metrics & Analytics',
                'lineage': 'Artifact Lineage & Provenance Tree'
            };
            document.getElementById('pageTitle').innerText = titles[viewName];
        }

        // Charts initialization
        const ctx1 = document.getElementById('lossChart').getContext('2d');
        new Chart(ctx1, {
            type: 'line',
            data: {
                labels: Array.from({length: 20}, (_, i) => `Epoch ${i*5}`),
                datasets: [
                    {
                        label: 'Training Loss',
                        data: [2.5, 1.9, 1.4, 1.1, 0.85, 0.65, 0.52, 0.41, 0.33, 0.28, 0.23, 0.19, 0.16, 0.14, 0.12, 0.11, 0.09, 0.08, 0.07, 0.06],
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Validation Accuracy (%)',
                        data: [45, 58, 67, 74, 80, 84, 88, 90, 92, 93.5, 94.8, 95.6, 96.2, 96.8, 97.4, 97.9, 98.2, 98.5, 98.7, 98.8],
                        borderColor: '#22c55e',
                        borderDash: [5, 5],
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#94a3b8' } } },
                scales: {
                    x: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        const ctx2 = document.getElementById('subsystemChart').getContext('2d');
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Experimentation', 'Metrics', 'Lineage', 'Data ETL', 'NLP', 'Vision', 'Tabular', 'RL', 'Server', 'UI'],
                datasets: [{
                    data: [10, 10, 9, 8, 4, 5, 4, 4, 8, 6],
                    backgroundColor: ['#38bdf8', '#22c55e', '#a855f7', '#f59e0b', '#ec4899', '#6366f1', '#14b8a6', '#84cc16', '#f43f5e', '#06b6d4']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 10 } } } }
            }
        });
    </script>
</body>
</html>
"""

class ResProtoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            res = {
                'status': 'ONLINE',
                'tests_passed': 30,
                'tests_total': 30,
                'repo_url': 'https://github.com/kondetivasanthi2002/ResProto-Hub.git'
            }
            self.wfile.write(json.dumps(res).encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    httpd = None
    for port in [9100, 9101, 9102, 9200]:
        try:
            httpd = socketserver.TCPServer(("127.0.0.1", port), ResProtoHandler)
            print(f"ResProto Hub Dashboard running on http://127.0.0.1:{port}")
            break
        except OSError:
            continue
    if httpd:
        httpd.serve_forever()
