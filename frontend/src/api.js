import axios from 'axios';

export const api = {
  error: null,
  loading: false,
  songs: [],
  now_playing_cover: require('./assets/cover2.jpg'),
  now_playing_title: 'Cafe Belga',
  now_playing_artist: 'Taco Hemingway',
  now_playing_freq: '90.0Hz',


  async getLs() {
    this.loading = true;
    try {
      let songs = (await axios.get('/ls')).data;
      this.loading = false;
      return songs;
    } catch (e) {
      this.processException(e);
      this.loading = false;
    }
  },


  async uploadFile(formData) {
    this.loading = true;
    try {
      this.clearError();
      await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      this.setSuccess('', 'Pomyślnie zmieniono avatar');
      this.loading = false;
    } catch (e) {
      this.processException(e);
      this.loading = false;
    }
  },

  processException(e) {
    if (typeof (e) === 'string')
      {this.setError(e);}
    else if (e.response && e.response.data && e.response.data.message)
        this.setError(e.response.data.title, e.response.data.message);
      else if (e.response && e.response.status)
        this.setError(`Nieznany błąd ${e.response.status}`, e);
      else
        this.setError("Nieznany błąd", e.toString());
  },

  setError(title, body) {
    if (!body)
      {this.error = {
        title: "Wystąpił błąd",
        body: title,
        isError: true,
      };}
    else
      {this.error = {
        title: title,
        body: body,
        isError: true,
      };}
  },

  setSuccess(title, body) {
    if (!body)
      {this.error = {
        title: "Sukces!",
        body: title,
        isError: false,
      };}
    else
      {this.error = {
        title: title,
        body: body,
        isError: false,
      };}
  },

  clearError() {
    this.error = null;
  },


};