# Master Prompt: Bloomberg-Type Terminal for Trading & Quantitative Research

## System Overview & Core Objective

Design and implement a comprehensive financial terminal system that rivals Bloomberg's functionality, specifically optimized for trading operations and quantitative research. The system should seamlessly integrate real-time market data, advanced analytics, execution capabilities, and research tools into a unified platform that serves both discretionary traders and systematic quantitative researchers.

## 1. Data Infrastructure & Architecture

### Real-Time Data Feeds
- **Market Data Integration**
  - Level 1, 2, and 3 market data across all asset classes (equities, fixed income, FX, commodities, derivatives, crypto)
  - Sub-millisecond latency requirements for HFT operations
  - Redundant data feed handlers with automatic failover
  - Normalized data models supporting multiple vendor formats (FIX, FAST, proprietary APIs)
  - Historical tick-by-tick data storage with compression algorithms

### Alternative Data Sources
- Satellite imagery integration for commodity/retail analysis
- Social media sentiment feeds with NLP processing
- News wire services with real-time parsing and entity recognition
- Economic indicators with revision tracking
- Corporate filings and regulatory disclosures
- Weather data for commodity and energy trading

### Data Quality & Validation
- Real-time anomaly detection algorithms
- Cross-vendor data reconciliation
- Corporate action adjustments automation
- Time-series alignment across different markets/timezones
- Data lineage tracking for audit trails

## 2. Trading Functionality

### Order Management System (OMS)
- Multi-asset class support with unified order entry
- Smart order routing with venue optimization
- Algorithmic trading integration (VWAP, TWAP, Implementation Shortfall, custom algos)
- Pre-trade compliance checks and position limits
- Real-time P&L calculation with multi-currency support
- Order staging and basket trading capabilities

### Execution Management
- Direct market access (DMA) to major exchanges
- Dark pool integration with liquidity aggregation
- Transaction cost analysis (TCA) in real-time
- Slippage monitoring and execution quality metrics
- Multi-leg strategy execution for complex derivatives

### Risk Management
- Real-time VaR calculations (Historical, Monte Carlo, Parametric)
- Stress testing with customizable scenarios
- Greeks calculation for options portfolios
- Correlation matrix updates with regime detection
- Margin requirement calculations across portfolios
- Counterparty risk monitoring

## 3. Quantitative Research Tools

### Backtesting Framework
- Event-driven simulation engine with realistic market microstructure
- Transaction cost modeling with market impact functions
- Multi-asset portfolio optimization with constraints
- Walk-forward analysis and out-of-sample testing
- Parameter sensitivity analysis and optimization
- Survivorship bias free data with point-in-time accuracy

### Statistical Analysis
- Factor model construction and testing
- Cointegration analysis for pairs trading
- Machine learning model integration (sklearn, TensorFlow, PyTorch)
- Time-series analysis tools (ARIMA, GARCH, state-space models)
- High-frequency data analysis with tick-level granularity
- Cross-sectional and panel data regression tools

### Strategy Development
- Visual strategy builder with drag-and-drop components
- Code editor with syntax highlighting for Python, R, C++, Julia
- Version control integration (Git)
- Collaborative research notebooks (Jupyter-style)
- Strategy performance attribution and decomposition
- Monte Carlo simulation for strategy robustness testing

## 4. Analytics & Visualization

### Charting Engine
- High-performance rendering for millions of data points
- 100+ technical indicators with customization
- Multi-timeframe analysis with synchronized cursors
- Volume profile and market microstructure visualization
- Option payoff diagrams and volatility surfaces
- 3D visualization for correlation matrices and risk surfaces

### Fixed Income Analytics
- Yield curve construction and interpolation
- Duration, convexity, and key rate duration calculations
- OAS (Option-Adjusted Spread) analysis
- Scenario analysis for interest rate movements
- Credit spread analysis and relative value tools
- Mortgage prepayment modeling

### Derivatives Analytics
- Real-time option Greeks with smile modeling
- Volatility surface calibration and arbitrage detection
- Exotic option pricing (Monte Carlo, finite difference)
- Structured product analysis and decomposition
- Counterparty credit risk (CVA, DVA, FVA)
- Cross-asset derivative strategies

## 5. User Interface & Experience

### Workspace Management
- Customizable layouts with saved workspace templates
- Multi-monitor support with window synchronization
- Tear-off windows and floating panels
- Dark/light themes with customizable color schemes
- Keyboard shortcuts with macro recording
- Touch-screen optimization for trading desks

### Search & Navigation
- Universal search bar with natural language processing
- Smart command palette (similar to VS Code)
- Contextual help system with interactive tutorials
- Bookmark system for frequently accessed functions
- History tracking with time-travel functionality

### Collaboration Features
- Integrated chat with compliance recording
- Screen sharing for remote collaboration
- Shared workspaces and analysis templates
- Commentary and annotation tools
- Alert sharing and distribution lists

## 6. Compliance & Surveillance

### Regulatory Reporting
- MiFID II/MiFIR transaction reporting
- Best execution reporting and analysis
- Position limit monitoring across venues
- Large trader reporting automation
- Dodd-Frank and EMIR compliance tools

### Trade Surveillance
- Pattern recognition for market manipulation
- Insider trading detection algorithms
- Wash trading and layering identification
- Front-running analysis
- Communication surveillance integration

## 7. System Architecture & Performance

### Technical Requirements
- Microservices architecture with container orchestration
- In-memory data grids for ultra-low latency
- Time-series databases optimized for financial data
- Message queuing with guaranteed delivery
- Horizontal scaling with automatic load balancing
- Edge computing for regional latency optimization

### Security & Access Control
- Multi-factor authentication with biometric support
- Role-based access control with granular permissions
- Data encryption at rest and in transit
- Audit logging with tamper-proof storage
- Secure API gateway for external integrations
- Hardware security module (HSM) integration

### Integration Capabilities
- RESTful and WebSocket APIs
- FIX protocol support for order routing
- Python/R/MATLAB integration libraries
- Excel add-in with real-time data binding
- Mobile applications (iOS/Android) with full functionality
- Third-party application marketplace

## 8. Advanced Features & Innovation

### Artificial Intelligence Integration
- Natural language query interface for data retrieval
- Anomaly detection in market behavior
- Predictive analytics for trade ideas
- Automated report generation
- Sentiment analysis from news and social media
- Deep learning for pattern recognition

### Blockchain & Digital Assets
- Cryptocurrency trading integration
- DeFi protocol monitoring
- Smart contract analysis tools
- On-chain data analytics
- Digital asset custody integration
- Tokenization platform connections

### Quantum Computing Readiness
- Quantum-resistant cryptography
- Portfolio optimization using quantum algorithms
- Option pricing with quantum Monte Carlo
- Infrastructure for quantum computing integration

## 9. Performance Metrics & SLAs

### System Performance
- 99.999% uptime with hot failover
- Sub-100 microsecond order latency
- 1 million messages/second throughput
- Petabyte-scale data storage
- Real-time replication across data centers

### User Experience Metrics
- Page load times under 200ms
- Search results in under 100ms
- Chart rendering at 60 FPS
- Concurrent user support: 10,000+
- API response times under 50ms

## 10. Implementation Considerations

### Development Approach
- Agile methodology with 2-week sprints
- Continuous integration/deployment pipeline
- A/B testing framework for features
- Performance regression testing
- Security scanning in CI/CD pipeline

### Technology Stack Recommendations
- Frontend: React/Vue.js with WebGL for visualizations
- Backend: Rust/C++ for performance-critical components
- Databases: TimescaleDB, kdb+, Redis
- Message Queue: Apache Kafka, Solace
- Container Orchestration: Kubernetes
- Monitoring: Prometheus, Grafana, ELK stack

### Deployment Strategy
- Phased rollout with pilot user groups
- Blue-green deployment for zero downtime
- Canary releases for risk mitigation
- Geographic distribution for latency optimization
- Disaster recovery with RPO < 1 minute

## Success Criteria

The terminal should achieve:
- Feature parity with Bloomberg Terminal core functionality
- Superior performance metrics in latency and throughput
- Intuitive UX reducing training time by 50%
- Cost reduction of 30-40% compared to incumbent solutions
- Extensibility allowing rapid feature development
- Regulatory compliance across major jurisdictions