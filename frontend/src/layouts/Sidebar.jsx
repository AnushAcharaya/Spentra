// Sidebar.jsx
import {
    ArrowLeftRight,
    Calculator,
    FolderOpen,
    HelpCircle,
    LayoutDashboard,
    LogOut,
    Settings,
    User,
    Wallet,
  } from "lucide-react";
  import { useNavigate } from "react-router-dom";
  
  export default function Sidebar() {
    const navigate = useNavigate()
    return (
      <div className="min-h-screen w-64 bg-gradient-to-b from-green-100 to-green-300 text-green-900 p-4 flex flex-col justify-between">
        <div>
          {/* Logo */}
          <div className="flex flex-col items-center mt-4 mb-8">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center">
              {/* Replace with your SVG logo */}
              <span className="text-white text-3xl font-bold">$</span>
            </div>
            <h1 className="mt-2 text-sm font-semibold tracking-wide">SPENTRA</h1>
          </div>
  
          {/* Nav Items */}
          <nav className="space-y-2">
            <NavItem
            onClick={() => navigate('/dashboard')}
            icon={<LayoutDashboard size={20} />} label="Dashboard" />
            <NavItem
              icon={<User size={20} />}
              label="Profile"
              onClick={() => navigate('profile')}
            />
            <NavItem
            onClick={() => navigate('budgets')}
            icon={<Wallet size={20} />} label="Budgets" active />
            <NavItem
             onClick={() => navigate('transaction')}
            icon={<ArrowLeftRight size={20} />} label="Transactions" />
            <NavItem icon={<FolderOpen size={20} />} label="Accounts" />
          </nav>
  
          <hr className="my-4 border-green-400" />
  
          <nav className="space-y-2">
            <NavItem icon={<Calculator size={20} />} label="Calculator" />
          </nav>
  
          <hr className="my-4 border-green-400" />
  
          <nav className="space-y-2">
            <NavItem icon={<Settings size={20} />} label="Settings" />
          </nav>
        </div>
  
        {/* Help & Logout */}
        <div className="space-y-2 mb-4">
          <NavItem icon={<HelpCircle size={20} />} label="Help" />
          <NavItem icon={<LogOut size={20} />} label="Logout" />
        </div>
      </div>
    );
  }
  
  function NavItem({ icon, label, active = false ,onClick}) {
    return (
      <div
      onClick={onClick}
        className={`flex items-center space-x-3 px-4 py-2 rounded-lg cursor-pointer ${
          active
            ? "bg-green-200 text-green-800"
            : "hover:bg-green-100 text-green-900"
        }`}
      >
        {icon}
        <span className="text-sm font-medium">{label}</span>
      </div>
    );
  }
  