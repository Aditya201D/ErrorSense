import { useEffect, useState } from "react";

function Sidebar({ history, onSelect, onClear, onDelete, collapsed, onToggle }) {
  const [hoveredId, setHoveredId] = useState(null);

  // Close sidebar on Escape
  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === "Escape" && !collapsed) {
        onToggle();
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [collapsed, onToggle]);

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return "Just now";
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return date.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    });
  };

  const truncate = (text, maxLength = 40) => {
    if (!text) return "";
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + "...";
  };

  return (
    <>
      {/* Mobile backdrop */}
      <div
        className={`sidebar-backdrop ${collapsed ? "" : "visible"}`}
        onClick={onToggle}
      />

      <aside
        className={`sidebar ${collapsed ? "collapsed" : "expanded"}`}
        aria-label="Recent searches"
      >
        <div className="sidebar-header">
          <div className="sidebar-title-row">
            {!collapsed && (
              <>
                <div className="sidebar-icon">🕘</div>
                <h3>Recent Searches</h3>
              </>
            )}
            {collapsed && <div className="sidebar-icon">🕘</div>}
            <button
              className="sidebar-toggle-btn"
              onClick={onToggle}
              aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
              title={collapsed ? "Expand" : "Collapse"}
            >
              {collapsed ? "›" : "‹"}
            </button>
          </div>

          {!collapsed && history.length > 0 && (
            <button
              className="sidebar-clear-all"
              onClick={onClear}
              title="Clear all history"
            >
              Clear All
            </button>
          )}
        </div>

        <div className="sidebar-content">
          {collapsed ? (
            <div className="sidebar-collapsed-list">
              {history.length === 0 ? (
                <div className="sidebar-empty-collapsed" title="No history yet">
                  ∅
                </div>
              ) : (
                history.slice(0, 8).map((item) => (
                  <button
                    key={item.id}
                    className="collapsed-dot"
                    onClick={() => onSelect(item)}
                    title={item.category || "Search"}
                  />
                ))
              )}
            </div>
          ) : history.length === 0 ? (
            <div className="sidebar-empty">
              <div className="sidebar-empty-icon">📋</div>
              <p className="sidebar-empty-title">No searches yet</p>
              <p className="sidebar-empty-subtitle">
                Your recent analyses will appear here
              </p>
            </div>
          ) : (
            <ul className="sidebar-list">
              {history.map((item) => (
                <li
                  key={item.id}
                  className="sidebar-item"
                  onMouseEnter={() => setHoveredId(item.id)}
                  onMouseLeave={() => setHoveredId(null)}
                >
                  <button
                    className="sidebar-item-btn"
                    onClick={() => onSelect(item)}
                    title="Load this search"
                  >
                    <div className="sidebar-item-category">
                      <span className="category-dot" />
                      {item.category || "Unknown"}
                    </div>
                    <div className="sidebar-item-snippet">
                      {truncate(item.request || item.response, 38)}
                    </div>
                    <div className="sidebar-item-meta">
                      <span className="sidebar-item-time">
                        {formatTime(item.timestamp)}
                      </span>
                      {item.confidence !== undefined && (
                        <span className="sidebar-item-confidence">
                          {typeof item.confidence === "number"
                            ? item.confidence.toFixed(1)
                            : item.confidence}
                          %
                        </span>
                      )}
                    </div>
                  </button>
                  <button
                    className={`sidebar-item-delete ${
                      hoveredId === item.id ? "visible" : ""
                    }`}
                    onClick={(e) => {
                      e.stopPropagation();
                      onDelete(item.id);
                    }}
                    title="Delete this entry"
                    aria-label="Delete entry"
                  >
                    ×
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {!collapsed && history.length > 0 && (
          <div className="sidebar-footer">
            <span>{history.length} search{history.length !== 1 ? "es" : ""}</span>
          </div>
        )}
      </aside>
    </>
  );
}

export default Sidebar;
