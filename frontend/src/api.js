/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const api = {
  error: null,
  loading: false,
  baseurl: '',
  songs: [],
  status: [],
  now_playing_cover: require('./assets/cover2.jpg'),
  now_playing_title: '',
  now_playing_artist: '',
  now_playing_freq: '90.0',


  async getLs() {
    this.loading = true;
    try {
      const songs = (await axios.get('/ls')).data;
      this.loading = false;
      return songs;
    } catch (e) {
      this.processException(e);
      this.loading = false;
    }
  },

  async getStatus() {
    this.loading = true;
    try {
      const status = (await axios.get('/status')).data;
      this.loading = false;
      return status;
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

  async startPlaying(file_name, freq, radio_text) {
    this.loading = true;
    try {
      this.clearError();
      await axios.post('/start', {
        file_name,
        freq,
        radio_text,
      });
      this.loading = false;
      // this.setSuccess('Sukces!', 'Rejestracja przebiegła pomyślnie. Proszę się zalogować.');
    } catch (e) {
      this.loading = false;
      this.processException(e);
    }
  },

  async stopPlaying() {
    this.loading = true;
    try {
      this.clearError();
      await axios.post('/stop');
      this.loading = false;
    } catch (e) {
      this.loading = false;
      this.processException(e);
    }
  },

  processException(e) {
    if (typeof (e) === 'string') {
      this.setError(e);
    } else if (e.response && e.response.data && e.response.data.message) {
      this.setError(e.response.data.title, e.response.data.message);
    } else if (e.response && e.response.status) {
      this.setError(`Nieznany błąd ${e.response.status}`, e);
    } else {
      this.setError('Nieznany błąd', e.toString());
    }
  },

  setError(title, body) {
    if (!body) {
      this.error = {
        title: 'Wystąpił błąd',
        body: title,
        isError: true,
      };
    } else {
      this.error = {
        title,
        body,
        isError: true,
      };
    }
  },

  setSuccess(title, body) {
    if (!body) {
      this.error = {
        title: 'Sukces!',
        body: title,
        isError: false,
      };
    } else {
      this.error = {
        title,
        body,
        isError: false,
      };
    }
  },

  clearError() {
    this.error = null;
  },


};
