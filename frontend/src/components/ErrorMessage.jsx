const ErrorMessage = ({ message }) => (
  <div className="bg-red-100 text-red-800 px-4 py-2 rounded mb-4 border border-red-300">
    <span className="font-semibold">Error:</span> {message}
  </div>
);

export default ErrorMessage; 