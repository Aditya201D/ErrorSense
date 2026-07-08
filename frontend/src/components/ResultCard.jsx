function ResultCard({ result }) {
    if (!result) {
        return (
            <div className="empty-state">
                <div className="empty-icon">🔍</div>

                <h3>Awaiting Analysis</h3>

                <p>Enter a request payload, response message, or both and click Analyse.</p>
            </div>
        );
    }

    return (
        <div className="result-container">
            <div className="result-section">
                <h3>Detected Issue</h3>

                <div className="issue-pill">{result.category}</div>
            </div>

            <div className="result-section">
                <h3>Confidence</h3>

                <div className="confidence-card">{result.confidence}%</div>
            </div>

            {result.severity && (
                <div className="result-section">
                    <h3>Severity</h3>

                    <div className={`severity severity-${result.severity.toLowerCase()}`}>{result.severity}</div>
                </div>
            )}

            <div className="result-section">
                <h3>Resolution</h3>

                <div className="resolution-card">{result.resolution}</div>
            </div>

            {result.possible_causes && result.possible_causes.length > 0 && (
                <div className="result-section">
                    <h3>Possible Causes</h3>

                    <ul className="info-list">
                        {result.possible_causes.map((cause, index) => (
                            <li key={index}>{cause}</li>
                        ))}
                    </ul>
                </div>
            )}

            {result.prevention && result.prevention.length > 0 && (
                <div className="result-section">
                    <h3>Prevention</h3>

                    <ul className="info-list">
                        {result.prevention.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </div>
            )}

            {result.documentation && (
                <div className="result-section">
                    <h3>Documentation</h3>

                    <div className="documentation-card">{result.documentation}</div>
                </div>
            )}

            {result.alternatives && result.alternatives.length > 0 && (
                <div className="result-section">
                    <h3>Alternative Matches</h3>

                    <div className="alternatives-grid">
                        {result.alternatives.map((item, index) => (
                            <div key={index} className="alternative-card">
                                <strong>{item.category}</strong>

                                <span>{item.confidence}%</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default ResultCard;
