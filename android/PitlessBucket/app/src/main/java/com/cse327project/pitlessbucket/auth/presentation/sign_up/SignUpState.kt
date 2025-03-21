package com.cse327project.pitlessbucket.auth.presentation.sign_up

data class SignUpState(
    val isSignInSuccessful: Boolean = false,
    val signInError: String? = null
)
