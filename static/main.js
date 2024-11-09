const characterPerLine = document.getElementById('cplRangeInput');
const characterPerLineValue = document.getElementById('cplRangeValue');

const contrast = document.getElementById('contrastRangeInput');
const contrastValue = document.getElementById('contrastRangeValue');

function updateRangeValue() {
	characterPerLineValue.textContent = characterPerLine.value;
	contrastValue.textContent = contrast.value;
}

characterPerLine.addEventListener("input", updateRangeValue);
contrast.addEventListener("input", updateRangeValue);
updateRangeValue()


document.getElementById('uploadForm').addEventListener('submit', async function(e) {
	e.preventDefault();

	const statusBar = document.getElementById('status-bar');
	const asciiOutput = document.getElementById('asciiOutput');
	const displayArea = document.getElementById('display');

	const fileInput = document.getElementById('fileInput');
	const formData = new FormData();

	const charSetSelect = document.getElementById('charSetSelect');
	const selectedCharSet = charSetSelect.value;

	const addColor = document.getElementById('addColor').checked;

	const screenWidth = window.screen.width
	let dynamicFontSize = 44 / characterPerLine.value;

	statusBar.innerHTML = "generating..."
	displayArea.style.border = "0px";
	asciiOutput.innerHTML = ""

	if (fileInput.files[0] == null) {
		statusBar.innerHTML = "No file selected!"
	} else {
		formData.append('file', fileInput.files[0]);

		try {
			const response = await fetch(`api/v1/image/upload?width=${characterPerLine.value}&character_set=${selectedCharSet}`, {
				method: 'POST',
				body: formData
			});

			const data = await response.json();
			const taskId = data["task_id"];
      let result;
      const eventSource = new EventSource(`http://127.0.0.1:7001/api/v1/image/tasks/${taskId}/stream`);
			statusBar.innerHTML = "started!";
			displayArea.style.border = "1px solid #FCFCFC";
			asciiOutput.style.fontSize = `${dynamicFontSize}rem`

      eventSource.onopen = () => {
        console.log('EventSource connected')
      }

      //eventSource can have event listeners based on the type of event.
      //Bydefault for message type of event it have the onmessage method which can be used directly or this same can be achieved through explicit eventlisteners
      eventSource.addEventListener('complete', (event) => {
        console.log(event.data)
        result = event.data;

        if (addColor == true) {
          asciiOutput.innerHTML = result;
        } else {
          asciiOutput.textContent = result;
        }

        eventSource.close();
      });


			if (response.status == 400) {
				statusBar.innerHTML = "Unsupported Image Format"
			}


		} catch (error) {
			statusBar.innerHTML = "Server Error!"
			console.error('Error:', error);
		}
	}
});
