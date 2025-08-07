def load_twin(manifest):
    twin = {
        'id': manifest.get('twinID'),
        'personas': manifest.get('personas'),
        'default': manifest.get('defaultPersona')
    }
    return twin
