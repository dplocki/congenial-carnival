// Log on gog.com
// Go to https://www.gog.com/account
await (async function() {
    const last_page = parseInt(document.querySelector('.list__pagination .pagin__total').textContent, 10);
    const result = [];
    let tags = {};

    for (let pageNumber = 1; pageNumber <= last_page; pageNumber++) {
        const request = await fetch(`https://www.gog.com/account/getFilteredProducts?hiddenFlag=0&mediaType=1&page=${pageNumber}&sortBy=date_purchased&totalPages=1`);
        const response = await request.json();
        tags = response.tags.reduce((result, tag) => { result[tag.id] = tag.name; return result; }, tags);

        for (const game of response.products) {
            if (game.isGame === false) {
                continue;
            }

            const title = game.title;
            const gameTags = game.tags.map(tagId => tags[tagId]);

            result.push({ title, tags: gameTags, id: game.id });
        }
    }

    return result;
})();
