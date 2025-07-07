const Utils = {
    formatarDataISOParaBR : (dataISO) => {
        if (!dataISO) return '';
        const date = new Date(dataISO);
        if (isNaN(date)) return '';
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = String(date.getFullYear());
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${day}/${month}/${year} ${hours}:${minutes}`;
    },

    removerNaoNumericos: (entrada) => {
        if (!entrada) return '';
        return String(entrada).replace(/\D+/g, '');
    }
}

window.Utils = Utils;