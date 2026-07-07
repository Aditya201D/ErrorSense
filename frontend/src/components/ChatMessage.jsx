function ChatMessage({ message }) {
    return (
      <div
        className={
          message.sender === "user"
            ? "message user"
            : "message bot"
        }
      >
        {message.sender === "user" ? (
          <p>{message.text}</p>
        ) : (
          <>
            <h4>{message.category}</h4>
            <p>{message.resolution}</p>
          </>
        )}
      </div>
    );
  }
  
  export default ChatMessage;