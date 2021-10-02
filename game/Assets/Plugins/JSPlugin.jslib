var plugin = {
    _ResultSave: function(score)
    {
        ResultSave(score);
    }
};

mergeInto(LibraryManager.library, plugin);