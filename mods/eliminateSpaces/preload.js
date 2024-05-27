(() => {
    const modUtils = window.modUtils;
	const start = Date.now();

	function del(passages, ...patterns) {
		for (let passage of passages) {
            let passageContent = modUtils.getPassageData(passage).content;
			for (let pattern of patterns) {
				passageContent = passageContent.replaceAll(pattern, '');
			}
            modUtils.updatePassageData(passage, passageContent, modUtils.getPassageData(passage).tags, 0);
        }
	}

    function delTN(passages) {
        del(passages, '\t', '\n');
    }

	function delTNS(passages) {
		del(passages, '\t', '\n', ' ');
	}

    function addSilently(passages) {
        for (let [passage, widgets] of Object.entries(passages)) {
            let passageContent = modUtils.getPassageData(passage).content;
            let re = new RegExp(`(?<=<<widget "(${widgets.join('|')})">>)(.|\n)+?(?=<<\/widget>>)`, 'g');
            passageContent = passageContent.replace(re, '<<silently>>$&<</silently>>');
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

	const start2 = Date.now();
	console.log(`EliminateSpaces: ${start2 - start}`);

    delTN([
		'Bog Lost',
		'Danube House Work',
		'English Play Late Role',
		'English Play Role Select',
		'Estate Cards Kiss',
		'Hospital Penis Enlargement',
		'Hospital Penis Reduction',
		'Moor Quicksand',
		'Street Bully Flash 2',
		'Whitney Rescue 2',
		'Whitney Rescue Break',
		'Widgets Text',
	]);

	delTNS([
		'Domus Tech Support Accept',
	]);

	console.log(`EliminateSpaces: ${Date.now() - start2}`);

})();
