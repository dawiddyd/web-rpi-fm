/* eslint-disable linebreak-style */
/* eslint-disable import/prefer-default-export */
import axios from 'axios';

export const api = {
  error: false,
  loading: false,
  baseurl: '',
  songs: [],
  status: [],
  now_playing_freq: '107.9',

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
      const status = [];
      this.loading = false;
      return status;
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
      this.setSuccess('', 'File send successfully');
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
      this.setError(`Unknown error ${e.response.status}`, e);
    } else {
      this.setError('Unknown error', e.toString());
    }
  },

  setError(title, body) {
    if (!body) {
      this.error = {
        title: 'An error occured',
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
        title: 'Success!',
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
