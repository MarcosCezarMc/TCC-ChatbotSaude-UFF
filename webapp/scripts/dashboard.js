const Dashboard = {

    contents: ['pacientes-list', 'paciente-detail', 'exames-list', 'exame-detail', 'alert-message'],
    listaPacientes: [],

    init: () => {
        Dashboard.setupButtons();
        Dashboard.setupInputMasks();
        Dashboard.showPacientesList();
    },

    setupButtons: () => {
        document.getElementById('popup-confirmar-agendamento').onclick = () => {
            Dashboard.agendarConfirmacaoPaciente();
        };
        document.getElementById('popup-confirmar-deletar').onclick = () => {
            Dashboard.deletePaciente();
        };
        document.getElementById('btn-voltar-paciente-detail').onclick = () => {
            Dashboard.showPacientesList();
        };
        document.getElementById('btn-criar-paciente').onclick = () => {
            Dashboard.showAddPaciente();
        };
        document.getElementById('btn-criar-paciente-detail').onclick = () => {
            Dashboard.adicionarPaciente();
        }
        document.getElementById('btn-editar-paciente-detail').onclick = () => {
            Dashboard.editarPaciente();
        }
    },

    setupInputMasks: () => {
        document.getElementById('nome').addEventListener('input', function (e) {
            let v = e.target.value.replace(/[0-9]/g, '');
            if (v.length > 80) v = v.slice(0, 80);
            e.target.value = v;
        });

        document.getElementById('cpf').addEventListener('input', function (e) {
            let v = e.target.value.replace(/\D/g, '');
            if (v.length > 11) v = v.slice(0, 11);
            v = v.replace(/(\d{3})(\d)/, '$1.$2');
            v = v.replace(/(\d{3})(\d)/, '$1.$2');
            v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = v;
        });

        document.getElementById('telefone').addEventListener('input', function (e) {
            let v = e.target.value.replace(/\D/g, '');
            if (v.length > 11) v = v.slice(0, 11);
            if (v.length > 0) v = v.replace(/(\d{0,2})/, '($1');
            if (v.length > 2) v = v.replace(/\((\d{2})(\d{0,5})/, '($1) $2');
            if (v.length > 7) v = v.replace(/(\d{5})(\d{1,4})$/, '$1-$2');
            e.target.value = v;
        });

        document.getElementById('data_nascimento').addEventListener('input', function (e) {
            let v = e.target.value.replace(/\D/g, '');
            if (v.length > 8) v = v.slice(0, 8);
            if (v.length >= 3) v = v.replace(/(\d{2})(\d{1,2})/, '$1/$2');
            if (v.length >= 6) v = v.replace(/(\d{2}\/\d{2})(\d{1,4})/, '$1/$2');
            e.target.value = v;
        });

        document.getElementById('email').addEventListener('input', function (e) {
            let v = e.target.value;
            if (v.length > 80) v = v.slice(0, 80);
            v = v.replace(/\s/g, '');
            e.target.value = v;
        });

        document.getElementById('rua').addEventListener('input', function (e) {
            let v = e.target.value;
            if (v.length > 80) v = v.slice(0, 80);
            e.target.value = v;
        });

        document.getElementById('numero').addEventListener('input', function (e) {
            let v = e.target.value;
            if (v.length > 16) v = v.slice(0, 16);
            e.target.value = v;
        });

        document.getElementById('bairro').addEventListener('input', function (e) {
            let v = e.target.value;
            if (v.length > 30) v = v.slice(0, 30);
            e.target.value = v;
        });

        document.getElementById('complemento').addEventListener('input', function (e) {
            let v = e.target.value;
            if (v.length > 35) v = v.slice(0, 35);
            e.target.value = v;
        });

        document.getElementById('cidade').addEventListener('input', function (e) {
            let v = e.target.value;
            if (v.length > 30) v = v.slice(0, 30);
            e.target.value = v;
        });

        document.getElementById('estado').addEventListener('input', function (e) {
            let v = e.target.value;
            if (v.length > 16) v = v.slice(0, 16);
            e.target.value = v;
        });

        document.getElementById('cep').addEventListener('input', function (e) {
            let v = e.target.value.replace(/\D/g, '');
            if (v.length > 8) v = v.slice(0, 8);
            if (v.length > 5) {
                v = v.replace(/(\d{5})(\d{1,3})/, '$1-$2');
            }
            e.target.value = v;
        });
    },

    hideAll: () => {
        for (const content of Dashboard.contents) {
            const element = document.getElementById(content);
            if (element) {
                element.style.display = 'none';
            }
        }
    },

    showAlert: (message) => {
        Dashboard.hideAll();
        const alertMessage = document.getElementById('alert-message');
        alertMessage.textContent = message;
        alertMessage.style.display = 'block';
    },

    showPacientesList: async () => {
        Dashboard.showAlert('Carregando lista de Pacientes...');
        const result = await window.Pacientes.listar();
        if (result.success) {
            Dashboard.listaPacientes = result.data;
            const pacientesList = document.getElementById('pacientes-list');
            const tbody = document.getElementById('pacientes-tbody');
            const template = document.getElementById('paciente-row-template');

            // Remove linhas antigas, exceto o template
            [...tbody.querySelectorAll('tr:not(#paciente-row-template)')].forEach(tr => tr.remove());

            let pacientePos = 0;
            for (const paciente of Dashboard.listaPacientes) {
                const cpfNumOnly = Utils.removerNaoNumericos(paciente.cpf);
                const rowIdentifier = `paciente-${pacientePos}-${cpfNumOnly}`;
                const row = template.cloneNode(true);

                row.id = `row-${rowIdentifier}`;
                row.style.display = '';
                row.querySelector('.paciente-nome').textContent = paciente.nome || 'Entrada inválida';
                row.querySelector('.paciente-cpf').textContent = paciente.cpf || 'Entrada inválida';
                row.querySelector('.paciente-n-exames').textContent = paciente.exames ? paciente.exames.length : 0;
                row.querySelector('.paciente-confirmado').textContent = paciente.confirmado ? '✅' : '❌';
                row.querySelector('.paciente-proxima-confirmacao').textContent =
                    Utils.formatarDataISOParaBR(paciente.proxima_interacao) !== ''
                        ? Utils.formatarDataISOParaBR(paciente.proxima_interacao)
                        : 'Não agendado';

                
                btnDetalhar = row.querySelector('.btn-detalhar');
                btnDetalhar.dataset.pacienteIndex = pacientePos;
                btnDetalhar.addEventListener('click', (e) => {
                    const pos = e.currentTarget.dataset.pacienteIndex;
                    const paciente = Dashboard.listaPacientes[pos];
                    Dashboard.showPacienteDetail(paciente);
                });

                btnEditar = row.querySelector('.btn-editar');
                btnEditar.dataset.pacienteIndex = pacientePos;
                btnEditar.addEventListener('click', (e) => {
                    const pos = e.currentTarget.dataset.pacienteIndex;
                    Dashboard.showEditPaciente(pos);
                });
                
                btnExames = row.querySelector('.btn-exames');
                btnExames.dataset.pacienteIndex = pacientePos;
                //TODO: listener

                btnAgendar = row.querySelector('.btn-agendar');
                btnAgendar.dataset.pacienteIndex = pacientePos;
                btnAgendar.addEventListener('click', (e) => {
                    const pos = e.currentTarget.dataset.pacienteIndex;
                    Dashboard.showPopupAgendarConfirmacao(pos);
                });

                btnDeletar = row.querySelector('.btn-deletar');
                btnDeletar.dataset.pacienteIndex = pacientePos;
                btnDeletar.addEventListener('click', async (e) => {
                    const pos = e.currentTarget.dataset.pacienteIndex;
                    Dashboard.showPopupDeletarPaciente(pos);
                });

                tbody.appendChild(row);
                pacientePos++;
            }
            Dashboard.hideAll();
            pacientesList.style.display = 'block';
        } else {
            Dashboard.showAlert(result.message);
        }
    },

    clearPopupAgendarConfirmacaoInput: () => {
        const input = document.getElementById('popup-agendar-datetime');
        input.value = '';
        if (input._flatpickr) input._flatpickr.destroy();
        flatpickr(input, {
            enableTime: true,
            dateFormat: 'H:i d-m-Y',
            minDate: 'today',
            time_24hr: true,
            allowInput: true
        });
    },

    agendarConfirmacaoPaciente: async () => {
        const input = document.getElementById('popup-agendar-datetime');
        const dataSelecionada = input.value;
        if (!dataSelecionada) {
            alert('Selecione uma data e hora.');
            return;
        }
        
        // Converte 'HH:MM DD-MM-YYYY' para ISO date 'YYYY-MM-DDTHH:MM:00'
        const [horaMinuto, diaMesAno] = dataSelecionada.split(' ');
        const [dia, mes, ano] = diaMesAno.split('-');
        const dataISO = `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}T${horaMinuto}:00`;

        const confirmarButton = document.getElementById('popup-confirmar-agendamento');
        confirmarButton.disabled = true;

        const pos = document.getElementById('popup-agendar-confirmacao').dataset.pacienteIndex;
        const paciente = Dashboard.listaPacientes[pos];
        const result = await window.Pacientes.agendarConfirmacao(paciente.id, dataISO);
        if (result.success) {
            Dashboard.listaPacientes[pos].proxima_interacao = dataISO;
            const rowIdentifier = `row-paciente-${pos}-${Utils.removerNaoNumericos(paciente.cpf)}`;
            const row = document.getElementById(rowIdentifier);
            row.querySelector('.paciente-proxima-confirmacao').textContent = Utils.formatarDataISOParaBR(dataISO);
            alert('Agendamento realizado com sucesso!');
        } else {
            Dashboard.showAlert(result.message || 'Erro ao agendar confirmação.');
        }

        document.getElementById('popup-agendar-confirmacao').style.display = 'none';
        confirmarButton.disabled = false;
    },

    showPopupAgendarConfirmacao: (selectedPacienteListPos) => {
        if(!window.flatpickr) {
            console.error('Não foi possível carregar o flatpickr.');
            showAlert('Erro: flatpickr não está disponível. Tente novamente mais tarde.');
            return;
        }

        Dashboard.clearPopupAgendarConfirmacaoInput();
        const popup = document.getElementById('popup-agendar-confirmacao');
        popup.dataset.pacienteIndex = selectedPacienteListPos;
        popup.style.display = 'flex';
    },  

    deletePaciente: async () => {
        const popup = document.getElementById('popup-deletar-confirmacao');
        const confirmarButton = document.getElementById('popup-confirmar-deletar');
        const cancelarButton = document.getElementById('popup-cancelar-deletar');
        confirmarButton.disabled = true;
        cancelarButton.disabled = true;

        const pos = popup.dataset.pacienteIndex;
        const paciente = Dashboard.listaPacientes[pos];
        const result = await window.Pacientes.deletar(paciente.id);
        if (result.success) {
            Dashboard.listaPacientes.splice(pos, 1);
            const rowIdentifier = `row-paciente-${pos}-${Utils.removerNaoNumericos(paciente.cpf)}`;
            const row = document.getElementById(rowIdentifier);
            row.remove();
            alert(`Paciente deletado com sucesso!`);
        }
        else alert(result.message || 'Contactar administrador com código de erro 2550');

        confirmarButton.disabled = false;
        cancelarButton.disabled = false;
        popup.style.display = 'none';
    },

    showPopupDeletarPaciente: (selectedPacienteListPos) => {
        const popup = document.getElementById('popup-deletar-confirmacao');
        popup.dataset.pacienteIndex = selectedPacienteListPos;
        const popUpText = document.getElementById('popup-deletar-paciente-nome');
        popUpText.textContent = `${Dashboard.listaPacientes[selectedPacienteListPos].nome}`;
        popup.style.display = 'flex';
    },

    showPacienteDetail: (paciente) => {
        Dashboard.showAlert('Carregando paciente ' + paciente.nome + '...');

        let form = document.getElementById('paciente-dados-form');
        form.reset();
        const grupoNumeroExames = form.querySelector('#numero_exames')?.closest('.form-group-paciente');
        grupoNumeroExames.style.display = '';
        for(const el of form.elements) el.disabled = true; 
        form.elements['nome'].value = paciente.nome || 'Não informado';
        form.elements['cpf'].value = paciente.cpf || 'Não informado';
        form.elements['telefone'].value = paciente.telefone || 'Não informado';
        form.elements['data_nascimento'].value = paciente.data_nascimento || 'Não informado'; 
        form.elements['email'].value = paciente.email || 'Não informado';
        form.elements['numero_exames'].value = paciente.exames ? paciente.exames.length : 0;
        form.elements['rua'].value = paciente.rua || 'Sem informação';
        form.elements['numero'].value = paciente.numero || 'Sem número';
        form.elements['bairro'].value = paciente.bairro || 'Sem informação';
        form.elements['complemento'].value = paciente.complemento || ' ';
        form.elements['cidade'].value = paciente.cidade || 'Sem informação';
        form.elements['estado'].value = paciente.estado || 'Sem UF';
        form.elements['cep'].value = paciente.cep || 'Sem CEP';

        const container = document.getElementById('paciente-detail-confirmacao');
        container.style.display = 'block';
        form = document.getElementById('paciente-confirmacao-form');
        form.reset();
        form.elements['confirmacao_nome'].value = paciente.confirmacao_nome || 'Sem confirmação';
        form.elements['confirmacao_cpf'].value = paciente.confirmacao_cpf || 'Sem confirmação';
        form.elements['confirmacao_telefone'].value = paciente.confirmacao_telefone || 'Sem confirmação';
        form.elements['confirmacao_data_nascimento'].value = paciente.confirmacao_data_nascimento
            ? Utils.formatarDataISOParaBR(paciente.data_nascimento)
            : 'Sem confirmação';
        form.elements['confirmacao_email'].value = paciente.confirmacao_email || 'Sem confirmação';
        form.elements['rua_confirmacao'].value = paciente.confirmacao_rua || 'Sem confirmação';
        form.elements['numero_confirmacao'].value = paciente.confirmacao_numero || 'Sem confirmação';
        form.elements['bairro_confirmacao'].value = paciente.confirmacao_bairro || 'Sem confirmação';
        form.elements['complemento_confirmacao'].value = paciente.confirmacao_complemento || 'Sem confirmação';
        form.elements['cidade_confirmacao'].value = paciente.confirmacao_cidade || 'Sem confirmação';
        form.elements['estado_confirmacao'].value = paciente.confirmacao_estado || 'Sem confirmação';
        form.elements['cep_confirmacao'].value = paciente.confirmacao_cep || 'Sem confirmação';
        form.elements['proxima_interacao'].value = paciente.proxima_interacao
            ? Utils.formatarDataISOParaBR(paciente.proxima_interacao)
            : 'Não está agendado';
        form.elements['ultima_interacao'].value = paciente.ultima_interacao
            ? Utils.formatarDataISOParaBR(paciente.ultima_interacao)
            : 'Nunca';
        form.elements['responsavel_confirmacao'].value = paciente.quem_confirmou || 'Não há';
        form.elements['canal_contato'].value = paciente.canal_contato || 'Não especificado';

        let btn = document.getElementById('btn-criar-paciente-detail');
        btn.style.display = 'none';
        btn = document.getElementById('btn-editar-paciente-detail');
        btn.style.display = 'none';

        Dashboard.hideAll();
        document.getElementById('paciente-detail').style.display = 'flex';
    },

    editarPaciente: async () => {
        const editarButton = document.getElementById('btn-editar-paciente-detail');
        editarButton.disabled = true;
        const voltarButton = document.getElementById('btn-voltar-paciente-detail');
        voltarButton.disabled = true;

        const nome = document.getElementById('nome').value.trim();
        const cpf = document.getElementById('cpf').value.trim();
        const telefone = document.getElementById('telefone').value.trim();
        if (!nome || !cpf || !telefone)  {          
            alert('Os campos Nome e Telefone são obrigatórios.');
            editarButton.disabled = false;
            voltarButton.disabled = false;
            return;
        }

        let paciente = {
            nome,
            cpf,
            telefone,
            data_nascimento: document.getElementById('data_nascimento').value.trim(),
            email: document.getElementById('email').value.trim(),
            rua: document.getElementById('rua').value.trim(),
            numero: document.getElementById('numero').value.trim(),
            bairro: document.getElementById('bairro').value.trim(),
            complemento: document.getElementById('complemento').value.trim(),
            cidade: document.getElementById('cidade').value.trim(),
            estado: document.getElementById('estado').value.trim(),
            cep: document.getElementById('cep').value.trim()
        };
        const paciente_id = Dashboard.listaPacientes[editarButton.dataset.pacienteIndex].id;

        const result = await window.Pacientes.editar(paciente_id, paciente);
        if (result.success) {
            alert('Paciente editado com sucesso!');
        } else {
            alert(result.message || 'Erro desconhecido');
        }

        editarButton.disabled = false;
        voltarButton.disabled = false;
        Dashboard.showPacientesList();
    },

    showEditPaciente: (selectedPacienteListPos) => {
        Dashboard.showAlert('Carregando formulário de edição de paciente...');

        const paciente = Dashboard.listaPacientes[selectedPacienteListPos];
        let form = document.getElementById('paciente-dados-form');
        form.reset();
        const grupoNumeroExames = form.querySelector('#numero_exames')?.closest('.form-group-paciente');
        grupoNumeroExames.style.display = '';
        for(const el of form.elements) el.disabled = false; 
        form.elements['nome'].value = paciente.nome || '';
        form.elements['cpf'].value = paciente.cpf || '';
        form.elements['cpf'].disabled = true;
        form.elements['telefone'].value = paciente.telefone || '';
        form.elements['data_nascimento'].value = paciente.data_nascimento || ''; 
        form.elements['email'].value = paciente.email || '';
        form.elements['numero_exames'].value = paciente.exames ? paciente.exames.length : 0;
        form.elements['rua'].value = paciente.rua || ' ';
        form.elements['numero'].value = paciente.numero || '';
        form.elements['bairro'].value = paciente.bairro || '';
        form.elements['complemento'].value = paciente.complemento || '';
        form.elements['cidade'].value = paciente.cidade || '';
        form.elements['estado'].value = paciente.estado || '';
        form.elements['cep'].value = paciente.cep || '';

        const container = document.getElementById('paciente-detail-confirmacao');
        container.style.display = 'none';

        let btn = document.getElementById('btn-editar-paciente-detail');
        btn.dataset.pacienteIndex = selectedPacienteListPos;
        btn.style.display = 'inline-block';
        btn = document.getElementById('btn-criar-paciente-detail');
        btn.style.display = 'none';

        Dashboard.hideAll();
        document.getElementById('paciente-detail').style.display = 'flex';
    },

    adicionarPaciente: async () => {
        const adicionarButton = document.getElementById('btn-criar-paciente-detail');
        adicionarButton.disabled = true;
        const voltarButton = document.getElementById('btn-voltar-paciente-detail');
        voltarButton.disabled = true;

        const nome = document.getElementById('nome').value.trim();
        const cpf = document.getElementById('cpf').value.trim();
        const telefone = document.getElementById('telefone').value.trim();
        if (!nome || !cpf || !telefone)  {          
            alert('Os campos Nome, CPF e Telefone são obrigatórios.');
            adicionarButton.disabled = false;
            voltarButton.disabled = false;
            return;
        }

        let paciente = {
            nome,
            cpf,
            telefone,
            data_nascimento: document.getElementById('data_nascimento').value.trim(),
            email: document.getElementById('email').value.trim(),
            rua: document.getElementById('rua').value.trim(),
            numero: document.getElementById('numero').value.trim(),
            bairro: document.getElementById('bairro').value.trim(),
            complemento: document.getElementById('complemento').value.trim(),
            cidade: document.getElementById('cidade').value.trim(),
            estado: document.getElementById('estado').value.trim(),
            cep: document.getElementById('cep').value.trim()
        };

        const result = await window.Pacientes.criar(paciente);
        if (result.success) {
            alert('Paciente adicionado com sucesso!');
        } else {
            alert(result.message || 'Erro desconhecido');
        }

        adicionarButton.disabled = false;
        voltarButton.disabled = false;
        Dashboard.showPacientesList();
    },

    showAddPaciente: () => {
        Dashboard.showAlert('Carregando formulário de adição de paciente...');

        const form = document.getElementById('paciente-dados-form');
        form.reset();
        grupoNumeroExames = form.querySelector('#numero_exames')?.closest('.form-group-paciente');
        grupoNumeroExames.style.display = 'none';
        for(const el of form.elements){
            el.disabled = false; 
        }

        const container = document.getElementById('paciente-detail-confirmacao');
        container.style.display = 'none';

        let btn = document.getElementById('btn-criar-paciente-detail');
        btn.style.display = 'inline-block';
        btn = document.getElementById('btn-editar-paciente-detail');
        btn.style.display = 'none';

        Dashboard.hideAll();
        document.getElementById('paciente-detail').style.display = 'flex';
    },

    showExamesList: () => {
        Dashboard.hideAll();
        document.getElementById('exames-list').style.display = 'block';

    },

    showExameDetail: () => {
        Dashboard.hideAll();
        document.getElementById('exame-detail').style.display = 'block';
    }

};


window.DashboardContents = Dashboard;