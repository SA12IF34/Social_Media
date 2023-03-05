import { useState, useRef, LegacyRef, MutableRefObject } from 'react'
import './App.css';
import api from './api/api';

function App() {

  const nameRef = useRef() as MutableRefObject<any>;
  const emailRef = useRef() as MutableRefObject<any>;
  const passwordRef = useRef() as MutableRefObject<any>;

  function getCookie(name: string) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    
}


  let csrftoken = getCookie('csrftoken');

  type imgType = string | ArrayBuffer | null | void ;


  async function callApi(desc: string, file: File) {
    try {
      const response = await api.post(
        "/posts/", 
        {
        desc: desc,
        file: file
        }, 
        {
        headers:{
          "Accept": "application/json",
          "Content-Type": "multipart/form-data",
          'X-CSRFToken': csrftoken
        }
      })
  
      if (response.status === 202) alert("It's Done Like A Profitional !");
      
    } catch (error: any) {
      alert(error.response.data['detail'])  
    }
  }

  function handleSubmit1(): void {
    let desc = document.getElementById("desc") as HTMLInputElement; 
    let inpt = document.getElementById("file") as HTMLInputElement;

    if (inpt.files![0]) {
      callApi(desc.value, inpt.files![0])
    } else {
      console.log("Shit");

    }
  }
  let shit = async ()=> {
    const res = await api.get("/");
    const data = await res.data
    return data;
  };
  async function handleSubmit2(): Promise<void> {
    console.log(shit())
    const response = await api.post('/', {
      account_name: `@${nameRef.current.value}`,
      name: nameRef.current.value,
      email: emailRef.current.value,
      password: passwordRef.current.value
    })
    if (response.status === 201) alert("everything is good !!")
  }

  
  

  return (
    <>
      <form onSubmit={(e) => {
        e.preventDefault();
        handleSubmit2();
      }} >
        <input type="text" name="name" id="name" ref={nameRef} placeholder='name' />
        <input type="email" name="email" id="email" ref={emailRef} placeholder='email' />
        <input type="password" name="password" id="password" ref={passwordRef} placeholder='password' />
        <input type="submit" value="submit" />
      </form>
      <form className='form-one' onSubmit={(e) => {
        e.preventDefault();
        handleSubmit1();
      }}>
        <input type="text"  id="desc" />
        <input type="file" id='file' />
        <input type="submit" value="submit" />
      </form>
    </>
  )
}

export default App
