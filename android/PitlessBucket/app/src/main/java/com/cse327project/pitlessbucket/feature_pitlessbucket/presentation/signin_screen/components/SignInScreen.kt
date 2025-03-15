package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.graphics.toColorInt
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.fontFamily

@Composable
fun SignInScreen(
    state: SignInState,
    onSignInClick: () -> Unit
) {
    val context = LocalContext.current
    LaunchedEffect(key1= state.signInError) {
        state.signInError?.let { error ->
            Toast.makeText(
                    context,
                    error,
                    Toast.LENGTH_LONG
                    ).show()
        }
    }
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(color = Color.White)
    ) {
        Column(
            modifier = Modifier
                .padding(top=250.dp, start = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "Welcome to",
                fontWeight = FontWeight.ExtraBold,
                fontSize = 50.sp
            )
            Text(
                text = "Pitless Bucket",
                fontFamily = fontFamily,
                fontWeight = FontWeight.ExtraBold,
                fontSize = 50.sp,
                color = Color("#3182ce".toColorInt())
            )
            Text(
                text = "Your private cloud storage aggregator application",
                fontWeight = FontWeight.SemiBold,
                fontSize = 16.sp,
            )
            Spacer(
                modifier = Modifier
                    .fillMaxHeight(.01f)
            )
            Button(onClick = onSignInClick) {
                Text(
                    text = "Sign in",
                    fontWeight = FontWeight.Bold,
                    fontSize = 25.sp
                    )
            }
        }
    }
}