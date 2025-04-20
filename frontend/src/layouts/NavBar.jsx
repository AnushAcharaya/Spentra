import { useEffect, useRef, useState } from "react";
import { NavLink } from "react-router-dom";

const navItems = [
  { name: "Home", path: "/" },
  { name: "About", path: "/#about" },
  { name: "Services", path: "/#services" },
  { name: "Why Us", path: "/#why" },
  { name: "Team", path: "/#team" },
  { name: "Login", path: "/login" }, // true route
];

const NavBar = () => {
  const [showSearch, setShowSearch] = useState(false);
  const searchRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSearch(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <nav className="flex items-center bg-gradient-to-r from-green-100 to-green-400 text-green-600 w-full">
      {/* Logo */}
      <div className="flex items-center gap-2 w-1/5">
        <img src="/images/logo.png" alt="SPENTRA Logo" className="w-40" />
      </div>

      {/* Navigation */}
      <div className="flex items-center gap-4 text-sm font-medium text-black list-none w-1/2">
        <div className="flex items-center justify-center gap-10 text-xl">
          {navItems.map((item) => (
            <NavLink
            className="text-[#7d7d7d] hover:text-black transition-colors ease-in-out duration-300"
            key={item.name} to={item.path}>
              {item.name}
            </NavLink>
          ))}
        </div>
      </div>

      {/* Search */}
      <div
        ref={searchRef}
        className={`w-1/5 flex justify-end items-center relative ${
          showSearch ? "border-b-[#000] border-b-2" : ""
        }`}
      >
        <div className="relative w-70">
          <input
            type="text"
            placeholder="Search..."
            className={`focus:outline-none outline-none text-black bg-transparent w-full transition-all duration-300 ${
              showSearch
                ? "opacity-100 pointer-events-auto"
                : "opacity-0 pointer-events-none"
            }`}
          />
        </div>
        <button
          onClick={() => setShowSearch((prev) => !prev)}
          aria-label="Toggle Search"
          className="p-1 rounded focus:outline-none ml-2"
        >
          <img className="w-7" src="images/search.png" alt="" />
        </button>
      </div>
    </nav>
  );
};

export default NavBar;
