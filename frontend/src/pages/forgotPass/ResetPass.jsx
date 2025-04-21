import React, { useState } from 'react';
import Input from './Input';
import Button from './Button';

const ResetPass = () => {
        const [pass, setPass] = useState('');
        const [confirmPass, setConfirmPass] = useState('')
    const handleSubmit = () =>{

    }
  return (
        <div className="w-full flex">
            <section className="flex w-1/2 justify-center items-center h-[100vh]">
                <div className="bg-[url('/bgImage.png')] h-[100vh] w-full bg-cover bg-center rounded-r-4xl">
                    <div className="flex flex-col justify-center items-center h-full">
                        <p className="text-[60px] text-white">Reset your</p>
                        <p className="text-[120px] text-white">Spentra</p>
                        <p className="text-[60px] text-white">Password for</p>
                        <p className="text-[60px] text-white">Account Access</p>
                    </div>
                </div>
            </section>
            <section className="flex flex-col w-1/2 items-center">
                <img 
                className='w-40'
                src="/logo.png" alt="Logo" />
                <div className="flex flex-col gap-5 w-110 h-120 bg-[#acdbac] rounded-3xl text-center">
                    <div className="flex flex-col gap-3">
                        <p className="uppercase font-bold text-4xl text-center mt-10">Set a new password</p>
                        <p className="text-[10px] text-center">
                            New password must be different from peviously used passwords
                        </p>
                    </div>
                    <div className="flex flex-col items-center gap-4">
                        <Input
                            eyes
                            placeholder="password"
                            value={pass}
                            onChange={(e) => setPass(e.target.value)}
                        />
                        <Input
                            eyes
                            placeholder="confirm password"
                            value={confirmPass}
                            onChange={(e) => setConfirmPass(e.target.value)}
                        />
                        <Button value="Reset Password" btn_type="gradient_btn" onClick={handleSubmit} />
                        {/* <Button value="Back" btn_type="white_btn" /> */}
                    </div>
                </div>
            </section>
        </div>
  )
}

export default ResetPass