const Footer = () => {
    return (
      <footer className="bg-gradient-to-r from-green-200 to-green-400 py-10 px-8 text-green-700">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Address Section */}
          <div>
            <h3 className="text-lg font-bold">Address</h3>
            <p className="flex items-center mt-2 text-green-700">
              <span className="mr-2 text-green-600">📍</span>Herald College,
              Kathmandu
            </p>
            <p className="flex items-center mt-2 text-green-700">
              <span className="mr-2 ">📞</span>9515606
            </p>
            <p className="flex items-center mt-2 text-green-700">
              <span className="mr-2 ">📧</span>spendra@gmail.com
            </p>
          </div>
  
          {/* Info Section */}
          <div>
            <h3 className="text-lg font-bold">Info</h3>
            <p className="mt-2 text-sm">
              Spentra simplifies expense tracking, ensuring better financial
              management. It uses AI-driven insights to help users stay on top of
              their budget.
            </p>
          </div>
  
          {/* Links Section */}
          <div>
            <h3 className="text-lg font-bold">Links</h3>
            <ul className="mt-2 space-y-1">
              <li>
                <a href="#" className="hover:underline">
                  Home
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  About
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  Service
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  Why us
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  Team
                </a>
              </li>
            </ul>
          </div>
  
          {/* Subscribe Section */}
          <div>
            <h3 className="text-lg font-bold">Subscribe</h3>
            <div className="mt-2">
              <input
                type="email"
                placeholder="Email"
                className="border-b border-gray-600 bg-transparent focus:outline-none w-full"
              />
              <button className="mt-3 bg-green-600 text-white px-4 py-2 rounded-full w-full hover:bg-green-700">
                Subscribe
              </button>
            </div>
          </div>
        </div>
      </footer>
    );
  };
  
  export default Footer;
  