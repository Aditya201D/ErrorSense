function ResultCard({ result }) {

  if (!result) {
    return (
      <div className="empty-state">

        <div className="empty-icon">
          🔍
        </div>

        <h3>
          Awaiting Analysis
        </h3>

        <p>
          Enter a request payload,
          response message,
          or both and click Analyse.
        </p>

      </div>
    );
  }

  return (
    <div className="result-container">

      <div className="result-section">

        <h3>
          Detected Issue
        </h3>

        <div className="issue-pill">
          {result.category}
        </div>

      </div>

      <div className="result-section">

        <h3>
          Suggested Resolution
        </h3>

        <div className="resolution-card">
          {result.resolution}
        </div>

      </div>

      {result.alternatives &&
        result.alternatives.length > 0 && (

        <div className="result-section">

          <h3>
            Alternative Matches
          </h3>

          <div className="alternatives-grid">

            {result.alternatives.map(
              (item, index) => (
                <div
                  key={index}
                  className="alternative-card"
                >
                  {item.category}
                </div>
              )
            )}

          </div>

        </div>

      )}

    </div>
  );
}

export default ResultCard;