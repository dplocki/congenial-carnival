// Log on https://www.epicgames.com/account
// Taken from Reddit: https://www.reddit.com/r/EpicGamesPC/comments/1epacr9/see_all_your_games_library_from_browser/
const fetchGamesList = async (pageToken = '', existingList = []) => {
    const data = await (await fetch(`https://www.epicgames.com/account/v2/payment/ajaxGetOrderHistory?sortDir=DESC&sortBy=DATE&nextPageToken=${pageToken}&locale=en-US`)).json();
    const gamesList = data.orders.reduce((acc, value) => [...acc, ...value.items.map(v => v.description)], []);
    console.log(`Orders: ${data.orders.length}, Games: ${gamesList.length}, Next Token: ${data.nextPageToken}`);

    const newList = [...existingList, ...gamesList];
    if (data.nextPageToken) {
        return await fetchGamesList(data.nextPageToken, newList);
    }

    return newList;
};

fetchGamesList().then(console.log);
