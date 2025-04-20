import React from 'react'

const Button = ({onClick, value, btn_type}) => {
    const btnStyles = {
        gradient_btn: "bg-gradient-to-r from-[#7ad97a] to-[#468546] text-white    ",
        white_btn:
          "bg-white text-black  ",
      };
  return (
        <div>
        <button 
        value={value}
        onClick={onClick}
        className={`${btnStyles[btn_type] || btnStyles.white_btn}  items-center gap-4 cursor-pointer p-3 w-100 rounded-2xl font-bold`}
         >
            {value || "Button"}
        </button>
    </div>
  )
}

export default Button