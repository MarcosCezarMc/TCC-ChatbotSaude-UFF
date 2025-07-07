const Pacientes = {    
    
    listar: async () => {
        try {
            const response = await fetch(`${window.API_CONFIG.baseURL}/pacientes`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${window.API_CONFIG.token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const pacientes = await response.json();
                return { success: true, data: pacientes };
            } else {
                const errorData = await response.json().catch(() => ({}));
                return { success: false, message: errorData.error || 'Erro ao listar pacientes' };
            }
        } catch (error) {
            console.error('Erro ao listar pacientes:', error);
            return { success: false, message: 'Erro de conexão com o servidor' };
        }
    },
    
    criar: async (paciente) => {
        try {
            const response = await fetch(`${window.API_CONFIG.baseURL}/pacientes`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${window.API_CONFIG.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(paciente)
            });

            if (response.ok) {
                const result = await response.json();
                return { success: true, data: result };
            } else {
                const errorData = await response.json().catch(() => ({}));
                return { success: false, message: errorData.error || 'Erro ao criar paciente' };
            }
        } catch (error) {
            console.error('Erro ao criar paciente:', error);
            return { success: false, message: 'Erro de conexão com o servidor' };
        }
    },
    
    editar: async (id, paciente) => {
        try {
            const response = await fetch(`${window.API_CONFIG.baseURL}/pacientes/id/${id}`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${window.API_CONFIG.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(paciente)
            });

            if (response.ok) {
                const result = await response.json();
                return { success: true, data: result };
            } else {
                const errorData = await response.json().catch(() => ({}));
                return { success: false, message: errorData.error || 'Erro ao editar paciente' };
            }
        } catch (error) {
            console.error('Erro ao editar paciente:', error);
            return { success: false, message: 'Erro de conexão com o servidor' };
        }
    },
    
    deletar: async (id) => {
        try {
            const response = await fetch(`${window.API_CONFIG.baseURL}/pacientes/id/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${window.API_CONFIG.token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 204) {
                return { success: true };
            } else {
                const errorData = await response.json().catch(() => ({}));
                return { success: false, message: errorData.error || 'Erro ao deletar paciente' };
            }
        } catch (error) {
            console.error('Erro ao deletar paciente:', error);
            return { success: false, message: 'Erro de conexão com o servidor' };
        }
    },

    agendarConfirmacao: async (id, dateISO) => {
        try {
            const response = await fetch(`${window.API_CONFIG.baseURL}/pacientes/id/${id}/agendar-contato`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${window.API_CONFIG.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ agendar_para: dateISO })
            });

            if (response.ok) {
                const result = await response.json();
                return { success: true, data: result };
            } else {
                const errorData = await response.json().catch(() => ({}));
                return { success: false, message: errorData.error || 'Erro ao agendar confirmação' };
            }
        } catch (error) {
            console.error('Erro ao agendar confirmação:', error);
            return { success: false, message: 'Erro de conexão com o servidor' };
        }
    }
};

window.Pacientes = Pacientes;
