// fetch JSON from Google Books API
async function grabVolumeInfo (volumeID) {
    let promise =  await fetch('https://www.googleapis.com/books/v1/volumes/' + volumeID);
      return promise.json()
    }

    // Grab volume ID from search results list to populate record details pane
    let title_links = document.querySelectorAll('tr');
    for (let i = 0; i < title_links.length; i++) {
      title_links[i].addEventListener('click', () => {
        let volumeID = title_links[i].getAttribute("data-record-id");
        let volume = grabVolumeInfo(volumeID)
          .then(volume => {
            let detailedView = document.getElementsByClassName('detailed-view');
            detailedView[0].removeAttribute('style');
            document.getElementById('cover').setAttribute('src', volume.volumeInfo.imageLinks.thumbnail)
            document.getElementById('title').innerHTML = 'Title: ' + volume.volumeInfo.title;
            document.getElementById('authors').innerHTML = 'Author(s): ' + volume.volumeInfo.authors;
            document.getElementById('publisher').innerHTML = 'Publisher: ' + volume.volumeInfo.publisher;
            document.getElementById('publicationDate').innerHTML = 'Publication Date: ' + volume.volumeInfo.publicationDate;
            document.getElementById('ISBN').innerHTML = 'ISBN: ' + volume.volumeInfo.industryIdentifiers[0].identifier;
            document.getElementById('description').innerHTML = volume.volumeInfo.description;
          })
      });
    }