const Button = ({ text, onClick }) => {
    return (
      <button
        onClick={onClick}
        className="bg-black text-green-500 border border-green-500 px-6 py-2 rounded hover:bg-green-500 hover:text-black transition text-lg"
      >
        ❯ {text}
      </button>
    );
  };
  
  export default Button;
  