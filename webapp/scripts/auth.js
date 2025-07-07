const Auth = {

    login: async (username, password) => {
        try {
            const response = await fetch(`${window.API_CONFIG.baseURL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    "username": username, 
                    "password": password 
                })
            });

            const data = await response.json();
              if (response.ok && data.token) {
                window.API_CONFIG.token = data.token;
                window.localStorage.setItem('authToken', data.token);
                
                return { success: true, message: 'Login realizado com sucesso!' };
            } else {
                return { success: false, message: data.error || 'Erro ao autenticar' };
            }
        } catch (error) {
            console.error('Erro no login:', error);
            return { success: false, message: 'Sem conexão com o servidor.' };
        }
    },

    logout: () => {
        window.API_CONFIG.token = null;
        window.localStorage.removeItem('authToken');
        return { success: true, message: 'Logout realizado com sucesso!' };
    },

    recoverLocalStorageAuth: () => {
        const token = window.localStorage.getItem('authToken');
        if (token) {
            window.API_CONFIG.token = token;
            return { authenticated: true, token: token };
        }
        return { authenticated: false, token: null };
    },

    isAuthenticated: () => {
        return window.API_CONFIG.token !== null && window.API_CONFIG.token !== undefined;
    },    
    
    validateAuth: async () => {
        if (!Auth.isAuthenticated()) {
            const reason = 'No token available';            
            window.dispatchEvent(new CustomEvent('invalidAuthentication', {
                detail: { 
                    message: 'Nenhum sessão de encontrada. Faça login novamente.',
                    reason: reason,
                    action: 'login_required'
                }
            }));
            return { valid: false, reason: reason };
        }

        try {
            const response = await fetch(`${window.API_CONFIG.baseURL}/validate-token`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${window.API_CONFIG.token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                return { valid: true, message: data.message };
            } 
            else if (response.status === 401 || response.status === 403) {
                const reason = 'Token expired or forbidden';
                window.dispatchEvent(new CustomEvent('invalidAuthentication', {
                    detail: { 
                        message: 'Sessão expirou. Faça login novamente.',
                        reason: reason,
                        httpStatus: response.status,
                        action: 'token_expired'
                    }
                }));
                return { valid: false, reason: reason };
            } 
            else {
                const reason = 'Invalid token or server error';
                window.dispatchEvent(new CustomEvent('invalidAuthentication', {
                    detail: { 
                        message: 'Sessão inválida. Faça login novamente.',
                        reason: reason,
                        httpStatus: response.status,
                        action: 'validation_failed'
                    }
                }));
                return { valid: false, reason: reason };
            }
        } catch (error) {
            console.error('Erro ao validar token com a API:', error);
            // Não dispara evento para erros de rede - pode ser temporário
            return { valid: false, reason: 'Network error' };
        }
    }
};

window.Auth = Auth;
