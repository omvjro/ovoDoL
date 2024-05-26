(() => {
    const modUtils = window.modUtils;

    function deleteTandN(passages) {
        for (let passage of passages) {
            let replaced = modUtils.getPassageData(passage).content.replaceAll(/\/\*(.|\n)*?\*\//g, '').replaceAll(/<!--(\n|.)*?-->/g, '').replaceAll('\n', '').replaceAll('\t', '');
            modUtils.updatePassageData(passage, replaced, ['widget'], 0);
        }
    }

    function addSilently(passages) {
        for (let [passage, widgets] of Object.entries(passages)) {
            let passageContent = modUtils.getPassageData(passage).content;
            let re = new RegExp(`(?<=<<widget "(${widgets.join('|')})">>)(.|\n)+?(?=<<\/widget>>)`, 'g');
            let patterns = passageContent.match(re);
            for (let pattern of patterns) {
                passageContent = passageContent.replace(pattern, `<<silently>>${pattern}<</silently>>`);
            }
            modUtils.updatePassageData(passage, passageContent, ['widget'], 0);
        }
    }

    addSilently({
        'Widgets Named Npcs': [
            'npc',
        ],
        'Widgets NPC Generation': [
            'generate1', 'generate2', 'generate3', 'generate4', 'generate5', 'generate6',
            'generatey1', 'generatey2', 'generatey3', 'generatey4', 'generatey5', 'generatey6',
            'generatev1', 'generatev2', 'generatev3', 'generatev4', 'generatev5', 'generatev6',
            'generateyv1', 'generateyv2', 'generateyv3', 'generateyv4', 'generateyv5', 'generateyv6',
            'generatep2', 'generatep3', 'generatep4', 'generatep5', 'generatep6',
            'generateyp2', 'generateyp3', 'generateyp4', 'generateyp5', 'generateyp6',
            'generates1', 'generates2', 'generates3', 'generates4', 'generates5', 'generates6',
        ]
    });

    // let allWidgetPassages = modUtils.getAllPassageData().filter(passage => passage.tags.includes('widget')).map(passage => passage.name);
    deleteTandN(['Widgets Text']);

})();
