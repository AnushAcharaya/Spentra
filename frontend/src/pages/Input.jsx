import React, {useState} from 'react'

const Input = ({placeholder, onChange, type , eyes=false, value}) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState("closed");
  
  const handleEyesOnClick = () => {
    setIsPasswordVisible((prevState) => !prevState);
  }

  return (
    <div className='flex bg-white rounded-2xl p-1 px-4  w-100 items-center  justify-between'>
        <input

        value={value}
        placeholder={placeholder}
        onChange={onChange}
        className={`w-100 h-12  placeholder:text-[#8c8c8c]  outline-none`}
        type={isPasswordVisible ? 'text' : 'password'} 
        />
        {eyes &&(
          <img 
          className='w-5'
          onClick={handleEyesOnClick}
          src={isPasswordVisible ? '/eyesOn.png' : '/eyesOff.png'}
           alt="" />
        )}
    </div>
  )
}

export default Input