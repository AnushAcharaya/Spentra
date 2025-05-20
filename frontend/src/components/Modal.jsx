const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white rounded shadow-lg w-full max-w-md p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 text-2xl font-bold focus:outline-none"
          aria-label="Close modal"
        >
          &times;
        </button>
        {title && <h2 className="text-xl font-bold mb-4 text-spentra-700">{title}</h2>}
        {children}
      </div>
    </div>
  );
};

export default Modal; 