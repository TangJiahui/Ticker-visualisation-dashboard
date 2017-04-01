function watchList() {
    var DEFAULT_VALUE = ["AAPL", "GOOG"];
    var STORAGE_KEY = "youya";

    var data;

    function getList() {
        return data;
    }

    function addToList(ticker) {
        ticker = ticker.toUpperCase();
        if (ticker === '' || data.indexOf(ticker) !== -1) {
            return false;
        }

        data.push(ticker);
        _saveToStorage();
        return true;
    }

    function deleteFromList(ticker) {
        ticker = ticker.toUpperCase();
        if (ticker === '' || data.indexOf(ticker) === -1) {
            return false;
        }

        data.splice(data.indexOf(ticker), 1);
        _saveToStorage();
        return true;
    }

    function _loadFromStorage() {
        data = JSON.parse(localStorage.getItem(STORAGE_KEY)) || DEFAULT_VALUE;
    }

    function _saveToStorage() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }

    _loadFromStorage();

    return {
        'getList': getList,
        'addToList': addToList,
        'deleteFromList': deleteFromList
    }
}
