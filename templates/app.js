document.addEventListener('DOMContentLoaded', function () {
    // 버튼에 이벤트 리스너 등록
    
  
    // 페이지 로드 시 데이터 불러오기
    fetchData();
  });
  
  const addButton = document.getElementById('addButton');
    addButton.addEventListener('click', createData);
    
  function fetchData() {
    // AJAX를 사용하여 서버에서 데이터를 가져옴
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            const dataList = document.getElementById('dataList');
            dataList.innerHTML = '';
  
            // 가져온 데이터를 목록으로 표시
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.data;
                dataList.appendChild(li);
            });
        });
  }
  
  function createData() {
    const dataInput = document.getElementById('dataInput');
    const data = dataInput.value;

    console.log('Sending data:', data); // 데이터를 콘솔에 출력

    // AJAX를 사용하여 서버에 데이터 전송
    fetch('/create_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data }),
    })
    .then(response => response.json())
    .then(() => {
        fetchData(); // 데이터 전송 후 목록 갱신
        dataInput.value = ''; // 입력창 초기화
    })
    .catch(error => console.error('데이터 생성 중 오류 발생:', error));
}
