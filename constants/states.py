(  # states
    # start
    START_STATE,
    # home
    HOME_STATE,
    DOWNLOAD_STATE,
    UPLOAD_STATE,
    LOGIN_STATE,
    INSIGHT_STATE,
    ADMIN_STATE,
    # login
    SET_POST_LINK_AND_GET_TYPE_OF_LOTTERY,
    IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN,
    LOGIN_WITH_TWO_FACTOR_AUTHENTICATION,
    # lottery
    LOTTERY,
    # upload
    IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN_IN_UPLOAD,
    LOGIN_WITH_TWO_FACTOR_AUTHENTICATION_FOR_UPLOAD,
    LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE,
    SET_MEDIA_TYPE_AND_GET_MEDIA,
    SET_MEDIA_AND_GET_CAPTION,
    SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT,
    SET_TITLE_OF_IGTV_AND_GET_CAPTION,
    VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM,
    # admin
    SEND_MESSAGE_TO_ALL_USER,
) = range(20)
