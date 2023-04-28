import React, { useState } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import axios from 'axios';

function App() {
  const [id, setId] = useState('');
  const [result, setResult] = useState([]);

  const handleIdChange = (event) => {
    setId(event.target.value);
  };

  const handleButtonClick = () => {
    console.log(`http://localhost:8080/user/${id}`)
    axios.get(`http://localhost:8080/user/${id}`)
      .then(response => {
        console.log(response.data)
        setResult(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  };
  const X = result.map((val, ids) => {
    if (val === null) {
      return <div></div>
    }
    const entries = Object.entries(val);  // 객체를 [key, value] 배열로 변환

    return (
      <div>
        {val.name}
        <img src={val.thumbnail} />
        {entries.map(([key, value]) => {  // 배열을 순회하며 출력
          if (value !== null) {  // 값이 null이 아닌 경우에만 출력
            if (key == "thumbnail" || key == "name") {
              return <div />
            }
            return (
              <div key={key}>
                <span>{key}: </span>
                <span>{value}</span>
              </div>
            );
          }
        })}
      </div>
    );
  })
  return (
    <div>
      <TextField
        label="아이디 입력"
        value={id}
        onChange={handleIdChange}
      />
      <Button variant="contained" color="primary" onClick={handleButtonClick}>
        확인
      </Button>
      <div>
        {X}
      </div>
    </div>
  );
}

export default App;