import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const getReviews = async () => {
    try {
        const response = await axios.get(`${API_URL}/reviews`);
        return response.data;
    } catch (error) {
        console.error("Error fetching reviews", error);
        return [];
    }
};
