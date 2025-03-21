package com.cse327project.pitlessbucket.file_manager.presentation.upload.components

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.cse327project.pitlessbucket.file_manager.presentation.upload.FileUploadState
import com.cse327project.pitlessbucket.file_manager.presentation.upload.FileUploadViewModel
import com.cse327project.pitlessbucket.auth.presentation.sign_up.UserData
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody

@Composable
fun FileUploadScreen(
    userData: UserData?,
    state: FileUploadState,
    navController: NavController,
    viewModel: FileUploadViewModel
) {
    val context = LocalContext.current

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let {
            viewModel.selectFile(it)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally
    ) {
        Text(
            text = "Select file for uploading"
        )
        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = { launcher.launch("*/*") }) {
            Text("Select File")
        }
        Spacer(modifier = Modifier.height(16.dp))

        state.selectedFileUri?.let { uri ->
            Text("Selected file: ${uri.path}")
        }
        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                state.selectedFileUri?.let { uri ->
                    val inputStream = context.contentResolver.openInputStream(uri)
                    val fileBytes = inputStream?.readBytes()
                    inputStream?.close()
                    if (fileBytes != null) {
                        val requestBody = fileBytes.toRequestBody("application/octet-stream".toMediaTypeOrNull())
                        val filePart = MultipartBody.Part.createFormData("file", "filename", requestBody)
                        val idToken = userData?.idToken ?: ""
                        viewModel.uploadFile(idToken, filePart)
                    }
                }
            },
            enabled = state.selectedFileUri != null && !state.isUploading
        ) {
            if (state.isUploading) {
                Text("Uploading...")
            } else {
                Text("Upload File")
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        if(state.isUploading){
            LoadingIndicator()
        }
        state.error?.let { error ->
            Text(text = "Error: $error", color = Color.Red)
        }
        state.uploadResponse?.let { response ->
            Text(text = "Upload successful: ${response.message}")
        }
    }
}

@Composable
private fun LoadingIndicator() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.TopCenter
    ) {
        CircularProgressIndicator()
    }
}
