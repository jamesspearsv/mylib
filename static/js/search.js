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
            let add_btn = document.getElementById('add-btn');
            let description_label = document.getElementById('description-label');
            add_btn.removeAttribute('style');
            description_label.removeAttribute('style');
            try {
              document.getElementById('cover').setAttribute('src', volume.volumeInfo.imageLinks.thumbnail)
            } catch {
              document.getElementById('cover').setAttribute('src', '/static/assests/blank-cover.svg')
            }
            document.getElementById('title').innerHTML = 'Title: ' + volume.volumeInfo.title;
            document.getElementById('authors').innerHTML = 'Author(s): ' + volume.volumeInfo.authors;
            document.getElementById('publisher').innerHTML = 'Publisher: ' + volume.volumeInfo.publisher;
            document.getElementById('publicationDate').innerHTML = 'Publication Date: ' + volume.volumeInfo.publishedDate;
            document.getElementById('ISBN').innerHTML = 'ISBN: ' + volume.volumeInfo.industryIdentifiers[0].identifier;
            document.getElementById('description').innerHTML = volume.volumeInfo.description;
            document.getElementById('add-to-catalog').setAttribute('value', volumeID)
          })
      });
    }