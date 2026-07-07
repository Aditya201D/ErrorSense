function ThemeToggle({ theme, onToggle }) {
  const isLight = theme === "light";
  return (
    <button
      className="theme-toggle"
      onClick={onToggle}
      title={isLight ? "Switch to dark theme" : "Switch to light theme"}
      aria-label={isLight ? "Switch to dark theme" : "Switch to light theme"}
    >
      <span className="theme-toggle-track">
        <span className={`theme-toggle-thumb ${isLight ? "thumb-light" : "thumb-dark"}`}>
          {isLight ? "☀" : "☾"}
        </span>
      </span>
    </button>
  );
}

export default ThemeToggle;
