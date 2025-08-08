DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS trocas;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE trocas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_ofertante_id INTEGER NOT NULL,
    produto_ofertado_id INTEGER NOT NULL,
    usuario_receptor_id INTEGER NOT NULL,
    produto_requisitado_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pendente' CHECK (
        status IN ('pendente', 'aceita', 'recusada')
    ),
    FOREIGN KEY (usuario_ofertante_id) REFERENCES usuarios(id),
    FOREIGN KEY (produto_ofertado_id) REFERENCES produtos(id),
    FOREIGN KEY (usuario_receptor_id) REFERENCES usuarios(id),
    FOREIGN KEY (produto_requisitado_id) REFERENCES produtos(id)
);
